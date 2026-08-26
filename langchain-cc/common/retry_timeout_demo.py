from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.runnables import RunnableLambda
import os

load_dotenv()


# ---------- RETRY EVIDENCE ----------

attempts = 0


def unstable_call(text):
    global attempts
    attempts += 1

    print(f"Retry attempt {attempts}")

    if attempts < 3:
        raise ConnectionError("Temporary failure")

    return "Retry succeeded"


retry_demo = RunnableLambda(unstable_call).with_retry(
    retry_if_exception_type=(ConnectionError,),
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)


# ---------- TIMEOUT EVIDENCE ----------

timeout_model = ChatOpenRouter(
    model="gpt-oss-120b",
    temperature=0,
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    max_retries=3,
    timeout=1
)


if __name__ == "__main__":

    print("RETRY EVIDENCE")

    result = retry_demo.invoke("test")
    print(result)

    # print("\nTIMEOUT EVIDENCE")

    # try:
    #     timeout_model.invoke("Explain LangChain in one sentence.")

    # except Exception as e:
    #     print(
    #         f"TIMEOUT FIRED: {type(e).__name__}: {e}"
        # )=== TIMEOUT EVIDENCE ===

#for timeout-
"""
Timeout is configured on model calls using timeout=30000.

A controlled test was also attempted with a deliberately very small timeout
to demonstrate the timeout firing. However, the ChatOpenRouter/OpenRouter
request did not terminate at the expected threshold during testing.

The timeout guard remains configured in Tasks 2–5. No timeout firing message
has been fabricated; this note records the attempted test and observed behaviour.
"""

