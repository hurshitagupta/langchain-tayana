import tiktoken

MAX_INPUT_TOKENS = 500

encoding = tiktoken.get_encoding("cl100k_base")


def check_token_budget(text: str):
    tokens = encoding.encode(text)
    token_count = len(tokens)

    if token_count > MAX_INPUT_TOKENS:
        raise ValueError(
            f"BUDGET REJECTED: input exceeds {MAX_INPUT_TOKENS} tokens."
        )

    return token_count


def validate_output(output):
    if not isinstance(output, str) or not output.strip():
        raise ValueError(
            "Error: invalid model output."
        )

    return output