# LangChain Architecture Assessment

This project builds a small question-answering application while focusing on clean architecture, dependency management, configuration, failure handling, and testability.

The project is developed incrementally, with each task extending the architecture created in the previous task.

---

## Task 1 — Layer Map

Task 1 separates the application into four layers:

* **Interface** — receives the user's question through the CLI.
* **Orchestration** — coordinates the application flow through `AnswerService`.
* **Capability** — defines the `Retriever` contract.
* **Infrastructure** — provides the concrete `SimpleRetriever` implementation.

### Run Task 1

```bash
python -m interface.cli "What is LangChain?"
```

### Tests

Task 1 contains two automated tests:

* **Success case** — verifies that the retriever returns the expected sources.
* **Failure case** — verifies the behaviour when the retriever raises an error.

Run:

```bash
python -m pytest -q
```

### Evidence

Terminal output from both the application and automated tests is saved in:

```text
results/task1_output.txt
```

The evidence can be generated using:

```bash
python -m interface.cli "What is LangChain?" > results\task1_output.txt
python -m pytest -q >> results\task1_output.txt
```

### Guardrails

Task 1 establishes the basic layer architecture without an LLM or external API call.

Runtime guardrails such as step limits, timeout, retry, token budget, and model-output validation will be introduced as the application gains the execution paths where those controls are required.

The final architecture will include the required guardrail implementations and evidence.

---

## Task 2 — Dependency Inversion

Task 2 extends the architecture by defining protocol interfaces for the three main dependencies:

* `Model`
* `Retriever`
* `Store`

Concrete implementations are injected into `AnswerService`, allowing the orchestration layer to depend on abstractions rather than specific implementations.

### Concrete Implementations

* **Model:** `OpenRouterModel` using LangChain `ChatOpenRouter`
* **Store:** Chroma vector store
* **Retriever:** LangChain retriever created from Chroma using `as_retriever()`
* **Embeddings:** Hugging Face `sentence-transformers/all-MiniLM-L6-v2`

Documents from `data/knowledge.txt` are split into chunks, embedded, stored in Chroma, and retrieved as relevant context before the model generates an answer.

### Run

```bash id="9gz8em"
python -m interface.cli "What is Langchain"
```

### Tests

Task 2 includes automated tests using injected fake dependencies to verify:

* Successful execution when dependencies behave normally.
* Failure behaviour when the retriever raises an exception.

Run:

```bash id="4yavsa"
python -m pytest tests/test_task2.py -q
```

### Evidence

Application and test output:

`results/task2_output.txt`

Guardrail evidence:

`results/task2_guardrails.txt`

### Guardrails

**Step limit:** A `StepCounter` places a hard limit on component/API hops. A deliberate third step with a limit of two produces `step_limit_reached`.

**Token budget:** The combined question and retrieved context are checked before the model call. Requests exceeding the configured budget are rejected.

**Validation:** Model output is validated before being returned. Empty or non-string output is rejected.

**Timeout:** The real `ChatOpenRouter` model is configured with a built-in request timeout. During testing, very small timeout values prevented normal model completion but did not consistently surface a clean timeout log through the integration, so the production value was restored.

**Retry:** The real `ChatOpenRouter` model uses its built-in capped retry configuration through `max_retries`. Retry behaviour is kept bounded rather than allowing unlimited attempts.

**Secret hygiene:** `OPENROUTER_API_KEY` is read from the environment and is not hardcoded in source code. The `.env` file is excluded from Git.

---

## Task 3 — Config Surface

Task 3 moves runtime configuration out of the application code and into environment variables.

A validated `Settings` object is implemented using Pydantic Settings. Components receive the validated settings instead of reading or hardcoding configuration independently.

### Configuration

The following values are loaded from the environment:

* Model name and OpenRouter base URL
* API key
* Retrieval `top_k`
* Timeout and retry limits
* Step limit and token budget
* Embedding model
* Chroma collection name
* Chunk size and overlap
* Knowledge file path

Pydantic validation ensures invalid configuration is rejected before the application runs. For example, `TOP_K=0` is rejected because `top_k` must be between 1 and 20.

The `.env` file is excluded from Git and secrets are accessed only through the validated settings object.

### Run

```bash
python -m interface.cli "What is Langchain?"
```

### Tests

Task 3 includes:

* **Success case** — verifies that valid environment configuration is loaded correctly.
* **Failure case** — verifies that invalid configuration is rejected with a Pydantic `ValidationError`.

Run:

```bash
python -m pytest tests/test_task3.py -q
```

### Evidence

Application and automated test output is saved in:

`results/task3_output.txt`

Guardrail evidence is saved in:

`results/task3_guardrails.txt`

### Guardrails

The reusable guardrails introduced previously remain active and their configurable values are now supplied through the validated settings surface.

* **Step limit** — `MAX_STEPS` controls the maximum allowed component/API hops.
* **Timeout** — `TIMEOUT_MS` configures the model request timeout.
* **Retry** — `MAX_RETRIES` provides a capped retry count for the model request.
* **Token budget** — `MAX_TOKENS` limits the question and retrieved context before the model call.
* **Validation** — model output is validated before it is returned.
* **Secret hygiene** — the OpenRouter API key is loaded from the environment and is never hardcoded in source code.

The step-limit, token-budget and validation failure paths are recorded through the reusable guardrail evidence script. Timeout and retry use the built-in `ChatOpenRouter` configuration.

---

## Task 4 — Failure Isolation

Task 4 makes retriever failure non-fatal.

The retriever call inside `AnswerService` is wrapped in exception handling. If retrieval succeeds, the returned documents are used normally. If the retriever fails, the failure is isolated instead of crashing the whole request.

On retriever failure:

* `docs` becomes an empty list
* `sources` becomes `0`
* the model is still called
* the request still returns an answer
* the `degraded` field records the failure type

Example degraded state:

```text
retriever_unavailable: RuntimeError
```

### Run

Normal application flow:

```bash
python -m interface.cli "What is LangChain?"
```

### Tests

Task 4 contains:

* **Success case** — verifies that a working retriever returns context normally and `degraded` is `None`.
* **Failure case** — injects a deliberately failing retriever and verifies that the request still returns an answer instead of crashing.

Run:

```bash
python -m pytest tests/test_task4.py -q 
```

The failure test prints the returned result so the degraded behaviour can be seen directly in the terminal.

Example:

```text
{
  'answer': 'Fallback answer',
  'sources': 0,
  'degraded': 'retriever_unavailable: RuntimeError'
}
```

A screenshot of the automated test output has also been included as evidence showing that retriever failure was captured correctly while the request still completed successfully.

### Evidence

Task 4 application and automated test evidence is saved in:

`results/task4_output.png`

Guardrail evidence is saved in:

`results/task4_guardrails.txt`

The automated test screenshot additionally shows the degraded failure behaviour being handled correctly.

### Guardrails

The same reusable guardrails remain active in Task 4:

* **Step limit** — limits component/API hops.
* **Timeout** — configured through the model request timeout.
* **Retry** — capped through the model retry configuration.
* **Token budget** — checks the question and retrieved context before the model call.
* **Validation** — validates model output before returning it.
* **Secret hygiene** — API keys are loaded only from environment variables and are not hardcoded.

Task 4 additionally introduces **failure isolation**, ensuring a retriever failure does not crash the complete request.

---

## Task 5 — Architecture Proof

Task 5 proves that the application architecture is not tied to its real infrastructure dependencies.

The real dependencies were replaced with fake implementations:

* `OpenRouterModel` → `FakeModel`
* `ChromaRetriever` → `FakeRetriever`
* `ChromaStore` → `FakeStore`
* validated settings → `FakeSettings`

The same `AnswerService` was used without modification.

This demonstrates that the orchestration layer depends on contracts and expected behaviour rather than specific infrastructure implementations.

### Tests

The automated architecture proof contains:

* **Success case** — all dependencies are replaced with fakes and `AnswerService` still successfully returns an answer.
* **Failure case** — a fake model deliberately returns invalid output, which is rejected by the existing validation guardrail.

Run:

```bash id="72o32d"
python -m pytest tests/test_task5.py -q -s
```

The successful architecture proof produces output similar to:

```text id="03ocqy"
{'answer': 'Fake model answer', 'sources': 1, 'degraded': None}
```

The failure case confirms that invalid fake model output is caught instead of being returned to the caller.

### Evidence

Automated test output:

`results/task5_output.txt`

Guardrail evidence:

`results/task5_guardrails.txt`

### Guardrails

The reusable guardrails remain active when dependencies are replaced:

* **Step limit** — caps component/API hops.
* **Timeout** — configured through the model request timeout.
* **Retry** — capped through model retry configuration.
* **Token budget** — prevents oversized input from reaching the model.
* **Validation** — prevents invalid model output from reaching the caller.
* **Secret hygiene** — secrets remain environment-based and are never hardcoded.

The failure test also demonstrates that the validation guardrail continues to work even when the real model is replaced with a fake.






