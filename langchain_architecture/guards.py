import tiktoken

class StepLimitExceeded(Exception):
    pass

class StepCounter:
    def __init__(self, max_steps:int):
        self.max_steps = max_steps
        self.steps = 0

    def check(self):
        self.steps +=1

        if self.steps>self.max_steps:
            raise StepLimitExceeded(
                f"Step Limit reached: {self.max_steps}" 
            )

class TokenBudgetExceeded(Exception):
    pass

def check_token_budget(text: str, max_tokens:int):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    if len(tokens)>max_tokens:
        raise TokenBudgetExceeded(
            f"Token Budget Exceeded: {len(tokens)} > {max_tokens}"
        )

class InvalidModelOutput(Exception):
    pass

def validate_model_output(output) -> str:
    if not isinstance(output, str):
        raise InvalidModelOutput("model_output_invalid: not a string")

    if not output.strip():
        raise InvalidModelOutput("model_output_invalid: empty response")

    return output