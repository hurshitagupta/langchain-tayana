class ChromaRetriever:
    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever()

    def search(self, query:str, k:int=4):
        docs = self.retriever.invoke(query)
        return docs[:k]
