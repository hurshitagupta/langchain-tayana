import sys

from infrastructure.retriever import ChromaRetriever
from infrastructure.model import OpenRouterModel
from infrastructure.store import ChromaStore
from infrastructure.indexer import index_file
from orchestration.answer_service import AnswerService

ques = sys.argv[1]

store = ChromaStore()

index_file("data/knowledge.txt", store)

retriever = ChromaRetriever(store.vector_store)

model = OpenRouterModel()

service= AnswerService(
    model=model,
    retriever=retriever,
    store=store
)
result = service.answer(ques)
print(result)