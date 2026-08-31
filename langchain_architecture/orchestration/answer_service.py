from capability.protocols import Retriever, Model, Store
from guards import StepCounter, check_token_budget, validate_model_output

class AnswerService:
    def __init__(self, retriever:Retriever, model:Model, store:Store):
        self.retriever = retriever
        self.model = model
        self.store = store

    def answer(self, question: str) -> dict:
        steps = StepCounter(max_steps=2)

        steps.check()
        docs = self.retriever.search(question, k=4)

        context = "\n".join(doc.page_content for doc in docs)

        prompt_text = question + "\n" + context
        check_token_budget(prompt_text, max_tokens=1000)

        steps.check()
        answer = self.model.generate(question, context)

        answer = validate_model_output(answer)

        return {
            "answer": answer,
            "sources": len(docs),
        }
