from .errors import LogprobsParserException
from .logprobs import build_json_logprobs
from .types import JSONLogprob, Token, ValueLogprob


class LogprobsResult:
    tokens: list[Token]

    _json_logprobs: JSONLogprob

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        self._json_logprobs = build_json_logprobs(self.tokens)

    def json_logprobs(self) -> JSONLogprob:
        """
        Returns the logprobs corresponding to the response.
        """
        return self._json_logprobs

    def object_logprobs(self) -> dict[str, JSONLogprob]:
        """
        Returns the logprobs corresponding to the response as an object. Throws
        if the response is not a JSON object.
        """
        if not isinstance(self._json_logprobs, dict):
            raise LogprobsParserException("response is not a json object")
        return self._json_logprobs

    def array_logprobs(self) -> list[JSONLogprob]:
        """
        Returns the logprobs corresponding to the response as an array. Throws
        if the response is not a JSON array.
        """
        if not isinstance(self._json_logprobs, list):
            raise LogprobsParserException("response is not a json array")
        return self._json_logprobs

    def primitive_logprobs(self) -> ValueLogprob:
        """
        Returns the logprobs corresponding to the response as a primitive. Throws
        if the response is not a JSON primitive.
        """
        if not isinstance(self._json_logprobs, ValueLogprob):
            raise LogprobsParserException("response is not a json primitive")
        return self._json_logprobs
