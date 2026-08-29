from capability.protocols import Retriever

class AnswerService:
    def __init__(self, retriever:Retriever):
        self.retriever = retriever

    def answer(self, ques:str) -> dict:
        docs = self.retriever.search(ques, 4)

        return{
            "ques":ques,
            "sources":len(docs),
            "context":list(docs)
        }
