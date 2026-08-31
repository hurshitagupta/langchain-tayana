from capability.protocols import Retriever, Model, Store
from guards import StepCounter, check_token_budget, validate_model_output
from config import Settings

class AnswerService:
    def __init__(self, retriever:Retriever, model:Model, store:Store, settings:Settings):
        self.retriever = retriever
        self.model = model
        self.store = store
        self.settings = settings

    def answer(self, question: str) -> dict:
        steps = StepCounter(max_steps=self.settings.max_steps)

        steps.check()
        docs = self.retriever.search(question, self.settings.top_k)

        context = "\n".join(doc.page_content for doc in docs)

        prompt_text = question + "\n" + context
        check_token_budget(prompt_text, self.settings.max_tokens)

        steps.check()
        answer = self.model.generate(question, context)

        answer = validate_model_output(answer)

        return {
            "answer": answer,
            "sources": len(docs),
        }
