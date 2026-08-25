import json
import sys
import time
import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")


model = ChatOpenRouter(
    model="gpt-oss-120b",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a precise assistant. Answer in one sentence."),
    ("human", "{question}"),
])

parser = StrOutputParser()


def run(question: str) -> dict:
    t0 = time.perf_counter()

    try:
        prompt_value = prompt.invoke({"question": question})
        response = model.invoke(prompt_value)
        output = parser.invoke(response)

        usage = response.usage_metadata or {}

        trace = {
            "question": question,
            "output": output,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "ms": round((time.perf_counter() - t0) * 1000),
            "success": True,
            "error": None,
        }

    except Exception as e:
        trace = {
            "question": question,
            "output": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "ms": round((time.perf_counter() - t0) * 1000),
            "success": False,
            "error": str(e),
        }

    print(json.dumps(trace, ensure_ascii=False))
    return trace


def summary(traces: list[dict]):
    report = {
        "runs": len(traces),
        "successful": sum(t["success"] for t in traces),
        "failed": sum(not t["success"] for t in traces),
        "total_tokens": sum(t["total_tokens"] for t in traces),
        "average_latency_ms": round(
            sum(t["ms"] for t in traces) / len(traces)
        ),
    }

    print(json.dumps({"summary": report}, ensure_ascii=False))
    return report


if __name__ == "__main__":
    questions = [
        "What is LangChain?",
        "What is LCEL?",
        "What is a Runnable?",
    ]

    traces = [run(question) for question in questions]

    summary(traces)