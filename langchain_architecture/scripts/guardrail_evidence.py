from guards import StepCounter, StepLimitExceeded, TokenBudgetExceeded, check_token_budget, validate_model_output, InvalidModelOutput

print("*****STEP LIMIT TEST******")
try:
    steps = StepCounter(max_steps=2)

    steps.check()
    print("Step1")

    steps.check()
    print("Step2")

    steps.check()

except StepLimitExceeded as exc:
    print(exc)

print("*****TOKEN BUDGET LIMIT********")

try:
    long_text = "LangChain " * 2000
    check_token_budget(long_text, max_tokens=100)
except TokenBudgetExceeded as exc:
    print(exc)


print("******VALIDATE MODEL OUTPUT*******")

try:
    validate_model_output("")

except InvalidModelOutput as exc:
    print(exc)