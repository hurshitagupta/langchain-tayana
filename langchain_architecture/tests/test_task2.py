from langchain_core.documents import Document
from orchestration.answer_service import AnswerService


class FakeModel:
    def generate(self, question: str, context: str) -> str:
        return "Fake answer"


class FakeRetriever:
    def search(self, query: str, k: int = 4):
        return [
            Document(page_content="Dependency inversion uses abstractions.")
        ]


class FakeStore:
    def add_documents(self, documents) -> None:
        pass


class FailingRetriever:
    def search(self, query: str, k: int = 4):
        raise RuntimeError("retriever failed")


def test_task2_success():
    service = AnswerService(
        model=FakeModel(),
        retriever=FakeRetriever(),
        store=FakeStore(),
    )

    result = service.answer("What is dependency inversion?")

    assert result["answer"] == "Fake answer"
    assert result["sources"] == 1


def test_task2_failure():
    service = AnswerService(
        model=FakeModel(),
        retriever=FailingRetriever(),
        store=FakeStore(),
    )

    try:
        service.answer("What is dependency inversion?")
        assert False
    except RuntimeError as exc:
        assert str(exc) == "retriever failed"