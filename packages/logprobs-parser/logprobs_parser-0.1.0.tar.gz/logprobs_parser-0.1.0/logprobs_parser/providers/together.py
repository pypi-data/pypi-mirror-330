from typing import TYPE_CHECKING

from ..result import LogprobsResult
from ..types import Token

if TYPE_CHECKING:
    try:
        from together.types import ChatCompletionResponse
    except ImportError:
        pass


class TogetherLogprobsResult(LogprobsResult):
    def __init__(self, completion: "ChatCompletionResponse"):
        tokens = _get_tokens(completion)
        super().__init__(tokens)


def _get_tokens(completion: "ChatCompletionResponse") -> list[Token]:
    if not completion.choices:
        return []

    logprobs = completion.choices[0].logprobs
    if not logprobs:
        return []

    return [
        Token(
            token=token,
            logprob=logprob,
            top_logprobs=[],
        )
        for token, logprob in zip(logprobs.tokens or [], logprobs.token_logprobs or [])
        if token is not None and logprob is not None
    ]
