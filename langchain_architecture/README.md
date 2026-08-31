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




