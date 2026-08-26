import pytest

from task3.runnable_contract import run_invoke, chain


def test_runnable_success():
    result = run_invoke("What is LCEL?")

    assert result["method"] == "invoke"
    assert isinstance(result["output"], str)
    assert len(result["output"].strip()) > 0
    assert result["ms"] >= 0


def test_runnable_failure():
    with pytest.raises(Exception):
        chain.invoke({})