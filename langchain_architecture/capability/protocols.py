from typing import Protocol, Sequence

class Retriever(Protocol):
    def search(self, ques:str, k:int=4) -> Sequence[str]:
        ...

class Model(Protocol):
    def generate(self, ques:str, context:str) -> str:
        ...

class Store(Protocol):
    def add_documents(self, documents) -> None:
        ...