from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import Settings

class ChromaStore:
    def __init__(self, settings:Settings):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )

        self.vector_store = Chroma(
            collection_name=settings.collection_name,
            embedding_function=self.embeddings
        )

    def add_documents(self,documents)->None:
        self.vector_store.add_documents(documents)

