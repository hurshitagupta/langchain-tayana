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


