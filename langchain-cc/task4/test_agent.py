import pytest

from task4.agent import add


def test_add_success():
    result = add.invoke({
        "a": 15,
        "b": 27
    })

    assert result == 42


def test_add_failure():
    with pytest.raises(Exception):
        add.invoke({
            "a": "hello",
            "b": 27
        })