import pytest

from infrastructure.retriever import SimpleRetriever
from orchestration.answer_service import AnswerService

class FailingRetriever:
        def search(self, query: str, k: int = 4):
            raise RuntimeError("retriever failed")

def test_answer_success():
      service = AnswerService(SimpleRetriever())
      result = service.answer("What is Langchain?")

      assert result["sources"]==2
      assert len(result["context"])==2

def test_answer_failure():
    service = AnswerService(FailingRetriever())

    try:
        result=service.answer("What is Langchain?")
        assert False

    except RuntimeError:
        assert True

     


