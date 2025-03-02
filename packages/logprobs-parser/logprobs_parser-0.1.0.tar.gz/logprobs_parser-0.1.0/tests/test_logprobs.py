import pytest

from logprobs_parser import LogprobsParserException, Token, build_json_logprobs
from logprobs_parser.types import ValueLogprob


def test_empty_tokens():
    with pytest.raises(LogprobsParserException):
        build_json_logprobs([])


def test_ignores_leading_garbage():
    tokens = [
        Token(token="```", logprob=-1),
        Token(token="json", logprob=-1),
        Token(token="\n", logprob=-1),
        Token(token="123", logprob=-2),
    ]
    assert build_json_logprobs(tokens) == ValueLogprob(value=123, logprob=-2, tokens=[Token(token="123", logprob=-2)])

    tokens = [
        Token(token="This", logprob=-1),
        Token(token="is", logprob=-1),
        Token(token="the", logprob=-1),
        Token(token="answer", logprob=-1),
        Token(token=":", logprob=-1),
        Token(token="123", logprob=-2),
    ]
    assert build_json_logprobs(tokens) == ValueLogprob(value=123, logprob=-2, tokens=[Token(token="123", logprob=-2)])


def test_ignores_trailing_garbage():
    tokens = [
        Token(token="123", logprob=-2),
        Token(token="\n", logprob=-1),
        Token(token="```", logprob=-1),
    ]
    assert build_json_logprobs(tokens) == ValueLogprob(value=123, logprob=-2, tokens=[Token(token="123", logprob=-2)])


def test_primitive_null():
    assert build_json_logprobs([Token(token="null", logprob=-1)]) == ValueLogprob(
        value=None, logprob=-1, tokens=[Token(token="null", logprob=-1)]
    )


def test_primitive_boolean():
    assert build_json_logprobs([Token(token="true", logprob=-1)]) == ValueLogprob(
        value=True, logprob=-1, tokens=[Token(token="true", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="false", logprob=-1)]) == ValueLogprob(
        value=False, logprob=-1, tokens=[Token(token="false", logprob=-1)]
    )


def test_primitive_number():
    assert build_json_logprobs([Token(token="0", logprob=-1)]) == ValueLogprob(
        value=0, logprob=-1, tokens=[Token(token="0", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="0.0", logprob=-1)]) == ValueLogprob(
        value=0, logprob=-1, tokens=[Token(token="0.0", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="-0.0", logprob=-1)]) == ValueLogprob(
        value=0, logprob=-1, tokens=[Token(token="-0.0", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="1", logprob=-1)]) == ValueLogprob(
        value=1, logprob=-1, tokens=[Token(token="1", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="-1", logprob=-1)]) == ValueLogprob(
        value=-1, logprob=-1, tokens=[Token(token="-1", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="1.23", logprob=-1)]) == ValueLogprob(
        value=1.23, logprob=-1, tokens=[Token(token="1.23", logprob=-1)]
    )

    assert build_json_logprobs([Token(token="-1.23", logprob=-1)]) == ValueLogprob(
        value=-1.23, logprob=-1, tokens=[Token(token="-1.23", logprob=-1)]
    )

    tokens = [
        Token(token="1", logprob=-1),
        Token(token="200", logprob=-2),
        Token(token=".", logprob=-3),
        Token(token="123", logprob=-4),
    ]
    assert build_json_logprobs(tokens) == ValueLogprob(value=1200.123, logprob=-10, tokens=tokens)


def test_primitive_string():
    assert build_json_logprobs([Token(token='""', logprob=-1)]) == ValueLogprob(
        value="", logprob=-1, tokens=[Token(token='""', logprob=-1)]
    )

    assert build_json_logprobs([Token(token='"hello"', logprob=-1)]) == ValueLogprob(
        value="hello", logprob=-1, tokens=[Token(token='"hello"', logprob=-1)]
    )

    assert build_json_logprobs([Token(token='"\\"hello\\""', logprob=-1)]) == ValueLogprob(
        value='"hello"', logprob=-1, tokens=[Token(token='"\\"hello\\""', logprob=-1)]
    )


def test_array():
    tokens = [
        Token(token="[", logprob=-1),
        Token(token="1", logprob=-2),
        Token(token=",", logprob=-3),
        Token(token="2", logprob=-4),
        Token(token="]", logprob=-5),
    ]
    assert build_json_logprobs(tokens) == [
        ValueLogprob(value=1, logprob=-2, tokens=[Token(token="1", logprob=-2)]),
        ValueLogprob(value=2, logprob=-4, tokens=[Token(token="2", logprob=-4)]),
    ]

    tokens = [
        Token(token="[ ", logprob=-1),
        Token(token=" 1 ", logprob=-2),
        Token(token=" , ", logprob=-3),
        Token(token=" 2 ", logprob=-4),
        Token(token=" ]", logprob=-5),
    ]
    assert build_json_logprobs(tokens) == [
        ValueLogprob(value=1, logprob=-2, tokens=[Token(token=" 1 ", logprob=-2)]),
        ValueLogprob(value=2, logprob=-4, tokens=[Token(token=" 2 ", logprob=-4)]),
    ]


def test_object():
    tokens = [
        Token(token="{", logprob=-1),
        Token(token='"key"', logprob=-2),
        Token(token=":", logprob=-3),
        Token(token="123", logprob=-4),
        Token(token="}", logprob=-5),
    ]
    assert build_json_logprobs(tokens) == {
        "key": ValueLogprob(value=123, logprob=-4, tokens=[Token(token="123", logprob=-4)])
    }
