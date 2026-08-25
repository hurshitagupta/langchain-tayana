import os
from dotenv import load_dotenv

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


model = ChatOpenRouter(
    model="gpt-oss-120b",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a precise assistant. Answer in one sentence."),
    ("human", "{question}")
])


parser = StrOutputParser()


# LCEL chain
chain = prompt | model | parser


questions = [
    "What is LangChain?",
    "What is LCEL?",
    "What is a Runnable in LangChain?",
    "What is an output parser?",
    "What is a retriever?",
]


def run():
    for question in questions:
        result = chain.invoke({
            "question": question
        })

        print(f"\nQuestion: {question}")
        print(f"Answer: {result}")


if __name__ == "__main__":
    run()