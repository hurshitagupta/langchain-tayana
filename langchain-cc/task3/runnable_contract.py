import asyncio
import json
import sys
import time
import os

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from common.guards import check_token_budget, validate_output

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")


model = ChatOpenRouter(
    model="gpt-oss-120b",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    timeout=30000,
    max_retries=3
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a precise assistant. Answer in one sentence."),
    ("human", "{question}"),
])

retry_model = model.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

chain = prompt | retry_model | StrOutputParser()


def run_invoke(question: str) -> dict:
    t0 = time.perf_counter()

    check_token_budget(question)

    output = chain.invoke({"question": question})

    output = validate_output(output)

    trace = {
        "method": "invoke",
        "question": question,
        "output": output,
        "ms": round((time.perf_counter() - t0) * 1000),
    }

    print(json.dumps(trace, ensure_ascii=False))
    return trace


def run_batch(questions: list[str]) -> dict:
    t0 = time.perf_counter()

    for question in questions:
        check_token_budget(question)

    inputs = [{"question": question} for question in questions]
    outputs = chain.batch(inputs)

    for output in outputs:
        validate_output(output)

    trace = {
        "method": "batch",
        "questions": questions,
        "outputs": outputs,
        "ms": round((time.perf_counter() - t0) * 1000),
    }

    print(json.dumps(trace, ensure_ascii=False))
    return trace


def run_stream(question: str) -> dict:

    check_token_budget(question)
    t0 = time.perf_counter()
    chunks = []

    for chunk in chain.stream({"question": question}):
        chunks.append(chunk)

    output = "".join(chunks)
    output = validate_output(output)

    trace = {
        "method": "stream",
        "question": question,
        "output": output,
        "ms": round((time.perf_counter() - t0) * 1000),
    }

    print(json.dumps(trace, ensure_ascii=False))
    return trace


async def run_ainvoke(question: str) -> dict:
    check_token_budget(question)
    t0 = time.perf_counter()

    output = await chain.ainvoke({"question": question})
    output = validate_output(output)

    trace = {
        "method": "ainvoke",
        "question": question,
        "output": output,
        "ms": round((time.perf_counter() - t0) * 1000),
    }

    print(json.dumps(trace, ensure_ascii=False))
    return trace


async def main():
    run_invoke("What is a Runnable in LangChain?")

    run_batch([
        "What is LCEL?",
        "What is a tool in LangChain?",
    ])

    run_stream("What is streaming in LangChain?")

    await run_ainvoke("What is asynchronous invocation in LangChain?")


if __name__ == "__main__":
    asyncio.run(main())