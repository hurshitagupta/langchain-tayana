import sys
from config import Settings
from infrastructure.retriever import ChromaRetriever
from infrastructure.model import OpenRouterModel
from infrastructure.store import ChromaStore
from infrastructure.indexer import index_file
from orchestration.answer_service import AnswerService

settings = Settings()

ques = sys.argv[1]

store = ChromaStore(settings)

index_file(settings.knowledge_path, store, settings)

retriever = ChromaRetriever(store.vector_store)

model = OpenRouterModel(settings)

service= AnswerService(
    model=model,
    retriever=retriever,
    store=store,
    settings=settings
)
result = service.answer(ques)
print(result)