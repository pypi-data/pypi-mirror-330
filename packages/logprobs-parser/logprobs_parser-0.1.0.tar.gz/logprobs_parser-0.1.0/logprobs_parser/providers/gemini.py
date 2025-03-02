from typing import TYPE_CHECKING

from ..result import LogprobsResult
from ..types import Token, TopLogprob

if TYPE_CHECKING:
    try:
        from google.genai.types import GenerateContentResponse
    except ImportError:
        pass


class GeminiLogprobsResult(LogprobsResult):
    def __init__(self, response: "GenerateContentResponse"):
        tokens = _get_tokens(response)
        super().__init__(tokens)


def _get_tokens(response: "GenerateContentResponse") -> list[Token]:
    if not response.candidates:
        return []

    logprobs = response.candidates[0].logprobs_result
    if not logprobs:
        return []

    tokens: list[Token] = []
    for candidate, top_candidates in zip(logprobs.chosen_candidates or [], logprobs.top_candidates or []):
        if candidate.token is None or candidate.log_probability is None:
            continue

        top_logprobs: list[TopLogprob] = []
        for top_candidate in top_candidates.candidates or []:
            if top_candidate.token is None or top_candidate.log_probability is None:
                continue

            top_logprobs.append(TopLogprob(token=top_candidate.token, logprob=top_candidate.log_probability))

        tokens.append(
            Token(
                token=candidate.token,
                logprob=candidate.log_probability,
                top_logprobs=top_logprobs,
            )
        )

    return tokens
