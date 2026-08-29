from typing import Protocol, Sequence

class Retriever(Protocol):
    def search(self, query:str, k:int=4) -> Sequence[str]:
        ...
