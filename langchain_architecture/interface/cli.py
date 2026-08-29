import sys

from infrastructure.retriever import SimpleRetriever
from orchestration.answer_service import AnswerService

ques = sys.argv[1]

retriever = SimpleRetriever()
service = AnswerService(retriever=retriever)

result = service.answer(ques)

print(result)