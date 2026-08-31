import os
from langchain_openrouter import ChatOpenRouter
from config import Settings

class OpenRouterModel:
    def __init__(self, settings:Settings):
        self.llm = ChatOpenRouter(
            model=settings.model_name,
            api_key=settings.openrouter_api_key,
            base_url=settings.base_url,
            # timeout=100, # this is for checking purpose
            timeout=settings.timeout_ms, 
            # max_retries=0 #this is for checking purpose
            max_retries=settings.max_retries
        )

    def generate(self, ques:str, context:str) -> str:
        result= self.llm.invoke(f"Question: {ques}, context:{context}")
        return result.content