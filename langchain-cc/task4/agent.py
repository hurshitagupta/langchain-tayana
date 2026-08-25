import json
import sys
import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


model = ChatOpenRouter(
    model="gpt-oss-120b",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

model_with_tools = model.bind_tools([add])


def run(question: str):
    messages = [("human", question)]

    response = model_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print("No tool was called.")
        return

    tool_call = response.tool_calls[0]
    result = add.invoke(tool_call["args"])

    trace = {
        "question": question,
        "tool": tool_call["name"],
        "arguments": tool_call["args"],
        "result": result
    }

    print(json.dumps(trace, ensure_ascii=False, indent=2))

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )

    final = model_with_tools.invoke(messages)

    print("Final answer:", final.content)


if __name__ == "__main__":
    run("Use the add tool to add 15 and 27.")