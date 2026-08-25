import pytest
from primitives import prompt, retriever, parser

def test_success_case():
    res = prompt.invoke({"question":"What is LCEL"})
    parser_val = parser.invoke("What is LCEL")
    docs = retriever.invoke("What is LCEL?")

    assert res is not None
    assert parser_val == "What is LCEL"
    assert isinstance(docs, list)
    assert len(docs) > 0 


def test_failure_case():
    with pytest.raises(Exception):
        prompt.invoke({})
