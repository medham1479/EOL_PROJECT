from transformers import pipeline

class LLMQuery:
    def __init__(self):
        self.model = pipeline('question-answering')

    def query(self, context, question):
        return self.model(question=question, context=context)