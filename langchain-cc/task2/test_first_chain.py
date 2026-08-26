import pytest
from task2.first_chain import chain


def test_chain_success():
    result = chain.invoke({
        "question": "What is LCEL?"
    })

    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_chain_failure():
    with pytest.raises(Exception):
        chain.invoke({})