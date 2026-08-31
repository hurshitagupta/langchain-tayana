from langchain_core.documents import Document

from orchestration.answer_service import AnswerService


class FakeSettings:
    max_steps = 2
    top_k = 4
    max_tokens = 1000


class FakeModel:
    def generate(self, question: str, context: str) -> str:
        return "Fallback answer"


class WorkingRetriever:
    def search(self, query: str, k: int = 4):
        return [Document(page_content="Useful context")]


class FailingRetriever:
    def search(self, query: str, k: int = 4):
        raise RuntimeError("retriever failed")


class FakeStore:
    def add_documents(self, documents) -> None:
        pass


def test_task4_success():
    service = AnswerService(
        retriever=WorkingRetriever(),
        model=FakeModel(),
        store=FakeStore(),
        settings=FakeSettings(),
    )

    result = service.answer("What is LangChain?")

    assert result["answer"] == "Fallback answer"
    assert result["sources"] == 1
    assert result["degraded"] is None


def test_task4_retriever_failure_degrades():
    service = AnswerService(
        retriever=FailingRetriever(),
        model=FakeModel(),
        store=FakeStore(),
        settings=FakeSettings(),
    )

    result = service.answer("What is LangChain?")

    print(result)

    assert result["answer"] == "Fallback answer"
    assert result["sources"] == 0
    assert result["degraded"] == "retriever_unavailable: RuntimeError"