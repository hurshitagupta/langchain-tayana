from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class ChromaStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            collection_name="architecture_docs",
            embedding_function=self.embeddings
        )

    def add_documents(self,documents)->None:
        self.vector_store.add_documents(documents)

