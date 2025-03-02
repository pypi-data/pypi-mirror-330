import re
from typing import Literal

import ijson
from ijson.common import IncompleteJSONError

from .errors import LogprobsParserException
from .types import JSONLogprob, Token, ValueLogprob

StackItem = Literal["start_map"] | Literal["start_array"] | tuple[Literal["map_key"], str] | JSONLogprob

_DELIMITER_RE = re.compile(r"(\{|\}|\[|\]|:|,)")


def build_json_logprobs(tokens: list[Token], use_float: bool = True) -> JSONLogprob:
    if not tokens:
        raise LogprobsParserException("no tokens provided")

    stack: list[StackItem] = []
    # List of (token index, token split) pairs.
    sent_token_splits: list[tuple[int, str]] = []

    @ijson.coroutine
    def handle_event():
        while True:
            event, value = yield

            match event:
                case "start_map":
                    stack.append(event)
                case "end_map":
                    _resolve_stack_object(stack)
                case "start_array":
                    stack.append(event)
                case "end_array":
                    _resolve_stack_array(stack)
                case "map_key":
                    stack.append(("map_key", value))
                case "null" | "boolean" | "integer" | "double" | "number" | "string":
                    filtered_token_splits = _filter_token_splits(sent_token_splits)
                    unique_token_indices = dict.fromkeys(i for i, _ in filtered_token_splits)
                    sent_tokens = [tokens[i] for i in unique_token_indices]
                    stack.append(
                        ValueLogprob(
                            value=value,
                            logprob=sum(t.logprob for t in sent_tokens),
                            tokens=sent_tokens,
                        )
                    )
                case _:
                    raise LogprobsParserException(f"unknown event: {event}")

            sent_token_splits.clear()

    coro = ijson.basic_parse_coro(handle_event(), use_float=use_float)

    for i, token in enumerate(tokens):
        # A single token may be relevant to multiple ijson events. For example, `":"` can be
        # used to separate a key from a string value in an object, and the leading quote char is
        # important to the logprob of the string value (as it distinguishes the value from a
        # non-string value). By splitting the token on these delimiters, we ensure that the token
        # is not solely consumed by the first ijson event.
        token_splits = _DELIMITER_RE.split(token.token)
        for split in token_splits:
            if not split:
                continue

            sent_token_splits.append((i, split))

            try:
                coro.send(split.encode())
            except IncompleteJSONError as e:
                if not len(stack):
                    # Ignore any invalid text before the JSON response.
                    coro = ijson.basic_parse_coro(handle_event())
                    sent_token_splits.clear()
                    continue
                if str(e).startswith("parse error: trailing garbage"):
                    # Ignore any invalid text after the JSON response.
                    break
                raise

    try:
        coro.close()
    except IncompleteJSONError as e:
        # Need to catch trailing garbage error here as well.
        if not str(e).startswith("parse error: trailing garbage"):
            raise

    if len(stack) != 1 or not isinstance(stack[0], (ValueLogprob, list, dict)):
        raise LogprobsParserException("invalid json")

    return stack[0]


def _filter_token_splits(token_splits: list[tuple[int, str]]) -> list[tuple[int, str]]:
    # Remove all whitespace and control characters from the beginning and end of the list.

    for i, (_, split) in enumerate(token_splits):
        start_split_idx = i
        if not split.isspace() and split not in (",", ":"):
            break

    for i, (_, split) in enumerate(reversed(token_splits)):
        end_split_idx = len(token_splits) - i
        if not split.isspace() and split not in (",", "]", "}"):
            break

    return token_splits[start_split_idx:end_split_idx]


def _resolve_stack_object(stack: list[StackItem]) -> None:
    items = []
    while stack:
        item = stack.pop()
        if item == "start_map":
            key_values = list(reversed(items))
            if len(key_values) % 2 != 0:
                raise LogprobsParserException("odd number of key value items")

            obj = {}
            for i in range(0, len(key_values), 2):
                key = key_values[i]
                value = key_values[i + 1]
                if not isinstance(key, tuple):
                    raise LogprobsParserException(f"invalid key item: {key}")

                # Every object value must be a valid JSON value.
                if not isinstance(value, (ValueLogprob, list, dict)):
                    raise LogprobsParserException(f"invalid value item: {value}")

                obj[key[1]] = value

            stack.append(obj)
            return

        items.append(item)

    raise LogprobsParserException("missing start_map event")


def _resolve_stack_array(stack: list[StackItem]) -> None:
    items = []
    while stack:
        item = stack.pop()
        if item == "start_array":
            stack.append(list(reversed(items)))
            return

        # Every array item must be a valid JSON value.
        if not isinstance(item, (ValueLogprob, list, dict)):
            raise LogprobsParserException(f"invalid array item: {item}")

        items.append(item)

    raise LogprobsParserException("missing start_array event")
