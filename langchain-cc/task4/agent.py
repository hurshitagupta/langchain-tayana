import json
import sys
import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

from common.guards import check_token_budget, validate_output

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
    base_url="https://openrouter.ai/api/v1",
    timeout=30000,
    max_retries=3
)

model_with_tools = model.bind_tools([add])

model_with_tools = model_with_tools.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

MAX_STEPS = 3

MAX_STEPS = 3


def check_step_limit(steps: int):
    if steps >= MAX_STEPS:
        raise RuntimeError(
            f"STEP LIMIT REACHED: maximum {MAX_STEPS} steps."
        )

def run(question: str):
    check_token_budget(question)

    messages = [("human", question)]
    steps = 0

    check_step_limit(steps)

    response = model_with_tools.invoke(messages)
    steps += 1

    messages.append(response)

    if not response.tool_calls:
        final_answer = validate_output(response.content)
        print("Final answer:", final_answer)
        return

    tool_call = response.tool_calls[0]
    result = add.invoke(tool_call["args"])

    trace = {
        "question": question,
        "tool": tool_call["name"],
        "arguments": tool_call["args"],
        "result": result,
    }

    print(json.dumps(trace, ensure_ascii=False, indent=2))

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"],
        )
    )

    check_step_limit(steps)

    final = model_with_tools.invoke(messages)
    steps += 1

    final_answer = validate_output(final.content)

    print("Final answer:", final_answer)


if __name__ == "__main__":
    run("Use the add tool to add 15 and 27.")