# LangChain Core Concepts Assignment

This assignment covers the core LangChain concepts through five incremental tasks. Each task builds on the previous one and includes working source code, execution evidence, and automated tests.

## Task 1 — Primitive Inventory

Implemented the basic LangChain primitives:

* Chat model
* Prompt template
* Output parser
* Retriever

The input and output schemas of each primitive are printed to demonstrate their Runnable contracts.

Task files are available under `task1/`.

## Task 2 — First Chain

Created the first LCEL chain using:

```python
prompt | model | parser
```

The chain is executed on five different inputs and returns a parsed string response for each.

Task files are available under `task2/`.

## Task 3 — Runnable Contract

Extended the LCEL chain to demonstrate:

* `invoke()`
* `batch()`
* `stream()`
* `ainvoke()`

Latency is recorded for every execution method using `time.perf_counter()`.

Task files are available under `task3/`.

## Task 4 — Tool + Agent

Implemented a simple tool-calling workflow in `task4/agent.py`.

A model is registered with an `add` tool and can request the tool when required. The tool name, arguments, result, and final model answer are logged.

A step limit is also applied to prevent uncontrolled model/tool execution.

## Task 5 — Trace Report

Implemented structured tracing in `task5/trace.py`.

Each run records:

* Input question
* Output
* Input tokens
* Output tokens
* Total tokens
* Latency
* Success/failure status
* Error details

A final summary reports total runs, successful runs, failures, total tokens, and average latency.

---

# Guardrails

Guardrails are applied where they are relevant to the execution pattern rather than being forced into tasks that do not execute a model or agent loop.

| Guardrail         | Implementation                                                        | Applied In   |
| ----------------- | --------------------------------------------------------------------- | ------------ |
| Step limit        | `MAX_STEPS` with explicit step checks                                 | Task 4       |
| Timeout           | Model-level `timeout` configuration                                   | Tasks 2–5    |
| Retry             | LangChain `.with_retry()` with capped attempts and exponential jitter | Tasks 2–5    |
| Token budget      | `check_token_budget()` before model execution                         | Tasks 2–5    |
| Output validation | `validate_output()` before returning model output                     | Tasks 2–5    |
| Secret hygiene    | API key loaded from environment and `.env` ignored by Git             | Project-wide |

Task 1 only performs primitive creation and schema inspection. It does not execute the model or an agent loop, therefore runtime model guardrails are not applicable there.

Shared guard logic is available in:

```text
common/guards.py
```

## Guardrail Evidence

Guardrail failures are intentionally triggered in controlled runs and saved as evidence.

Examples include:

```text
BUDGET REJECTED: input exceeds allowed token budget.

QUARANTINED: invalid model output.

STEP LIMIT REACHED: maximum steps exceeded.

Retry attempt 1
Retry attempt 2
Retry attempt 3
Retry succeeded
```

Task-specific guardrail evidence is stored in the corresponding `guardrail_logs.txt` files.

Timeout and retry evidence is stored separately at the assignment level.

---

# Secret Hygiene

API keys are never hardcoded in the source code.

The OpenRouter API key is loaded through environment variables using `.env`.

The `.env` file is excluded from Git using `.gitignore`.

Secret hygiene can be verified using:

```bash
git check-ignore .env
```

The expected result is:

```text
.env
```

This confirms that the environment file containing the API key is excluded from version control.

---

# Running the Tasks

Run commands from the `langchain-cc` directory.

### Task 1

```bash
python -m task1.primitives
```

### Task 2

```bash
python -m task2.first_chain
```

### Task 3

```bash
python -m task3.runnable_contract
```

### Task 4

```bash
python -m task4.agent
```

### Task 5

```bash
python -m task5.trace
```

---

# Automated Tests

Each task contains automated tests covering a success case and a failure case.

Tests can be executed individually or together using:

```bash
pytest -v
```

This verifies the core LangChain functionality together with the implemented failure handling.
