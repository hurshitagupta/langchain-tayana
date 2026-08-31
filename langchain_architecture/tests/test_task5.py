from langchain_core.documents import Document
from orchestration.answer_service import AnswerService


class FakeModel:
    def generate(self, question: str, context: str) -> str:
        return "Fake model answer"


class FakeRetriever:
    def search(self, query: str, k: int = 4):
        return [
            Document(page_content="Fake retrieved document")
        ]


class FakeStore:
    def add_documents(self, documents) -> None:
        pass


class FakeSettings:
    max_steps = 2
    top_k = 4
    max_tokens = 1000


def test_all_dependencies_can_be_swapped():
    service = AnswerService(
        model=FakeModel(),
        retriever=FakeRetriever(),
        store=FakeStore(),
        settings=FakeSettings(),
    )

    result = service.answer("Test question")

    print(result)

    assert result["answer"] == "Fake model answer"
    assert result["sources"] == 1
    assert result["degraded"] is None

class FailingFakeModel:
    def generate(self, question: str, context: str) -> str:
        return ""


def test_fake_model_invalid_output():
    service = AnswerService(
        model=FailingFakeModel(),
        retriever=FakeRetriever(),
        store=FakeStore(),
        settings=FakeSettings(),
    )

    try:
        service.answer("Test question")
        assert False

    except Exception as exc:
        print(f"Failure correctly caught: {exc}")
        assert "model_output_invalid" in str(exc)