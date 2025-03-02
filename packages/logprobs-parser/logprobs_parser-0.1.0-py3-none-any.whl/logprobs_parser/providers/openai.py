from typing import TYPE_CHECKING

from ..result import LogprobsResult
from ..types import Token, TopLogprob

if TYPE_CHECKING:
    try:
        from openai.types.chat import ChatCompletion
    except ImportError:
        pass


class OpenAILogprobsResult(LogprobsResult):
    def __init__(self, completion: "ChatCompletion"):
        tokens = _get_tokens(completion)
        super().__init__(tokens)


def _get_tokens(completion: "ChatCompletion") -> list[Token]:
    if not completion.choices:
        return []

    logprobs = completion.choices[0].logprobs
    if not logprobs:
        return []

    content = logprobs.content
    if not content:
        return []

    return [
        Token(
            token=token.token,
            logprob=token.logprob,
            top_logprobs=[TopLogprob(token=t.token, logprob=t.logprob) for t in token.top_logprobs],
        )
        for token in content
    ]
