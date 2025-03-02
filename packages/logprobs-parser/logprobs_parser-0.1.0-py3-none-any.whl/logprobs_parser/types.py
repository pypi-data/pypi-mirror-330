from typing import Any

from pydantic import BaseModel, Field


class TopLogprob(BaseModel):
    """
    One of the top N most likely tokens.
    """

    token: str
    logprob: float


class Token(BaseModel):
    """
    A token outputted by the model.
    """

    token: str
    logprob: float
    top_logprobs: list[TopLogprob] = Field(default_factory=list)


class ValueLogprob(BaseModel):
    """
    The logprob and tokens comprising a primitive value in the model's JSON output.
    """

    value: Any
    logprob: float
    tokens: list[Token]


JSONLogprob = ValueLogprob | list["JSONLogprob"] | dict[str, "JSONLogprob"]
JSONArrayLogprob = list[JSONLogprob]
JSONObjectLogprob = dict[str, JSONLogprob]
