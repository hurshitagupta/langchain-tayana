import os
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv

load_dotenv()

class OpenRouterModel:
    def __init__(self):
        self.llm = ChatOpenRouter(
            model="openai/gpt-oss-120b",
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
            # timeout=100, # this is for checking purpose
            timeout=30_000, #30sec
            # max_retries=0 #this is for checking purpose
            max_retries=2
        )

    def generate(self, ques:str, context:str) -> str:
        result= self.llm.invoke(f"Question: {ques}, context:{context}")
        return result.content