# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import typing

import utila

import german


def search(
        tokens: list,
        sentence: list,
        lowercase: bool = True,
        tokens_complex: bool = True,
) -> list:
    # prepare data
    if isinstance(tokens, str):
        tokens = german.split_words(tokens, validate_sentences=False)
    if isinstance(sentence, str):
        sentence = german.split_words(sentence, validate_sentences=False)
    tokens_length = len(tokens)
    if tokens_length > len(sentence):
        return []
    if lowercase:
        tokens = [lower(item) for item in tokens]
        sentence = [lower(item) for item in sentence]
    sentence = [german.wordtypes(word) for word in sentence]
    if tokens_complex:
        tokens = [german.wordtypes(token) for token in tokens]
    # start searching
    result = []
    for start in range(len(sentence) - len(tokens) + 1):
        selected = sentence[start:start + tokens_length]
        if not _match(tokens, selected, tokens_complex):
            continue
        result.append((start, start + tokens_length))
    # improve result
    result = utila.make_unique(result)
    return result


def searches(
        tokenslist: list,
        sentence: list,
        lowercase: bool = True,
        tokens_complex: bool = True,
) -> list:
    result = []
    for tokens in tokenslist:
        matches = search(tokens, sentence, lowercase, tokens_complex)
        if matches:
            result.extend(matches)
    # TODO: SORT RESULT?
    result = utila.make_unique(result)
    return result


def lower(item: typing.Any) -> typing.Any:
    with contextlib.suppress(AttributeError):
        return item.lower()
    return item


def _match(chunk: list, expected: list, token_complex) -> bool:
    assert len(chunk) == len(expected)
    for item, item_expected in zip(chunk, expected):
        if token_complex:
            if not item & item_expected:
                return False
        else:
            if item not in item_expected:
                return False
    return True
