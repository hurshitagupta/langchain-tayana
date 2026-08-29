class SimpleRetriever:
    def search(self, query:str, k:int=4):
        docs=[
            "LangChain helps developers build applications using language models.",
            "A retriever finds relevant information for a user's question.",
        ]
        return docs[:k]
