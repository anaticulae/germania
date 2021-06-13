# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import konrad
import konrad.mark

import german


def extract_quotes(items: str, lang=konrad.GERMAN) -> list:  # pylint:disable=W0613
    assert isinstance(items, str), type(items)
    tokens = german.word_tokenize(items, validate_sentences=False)
    result = []

    doubled = parse_quotation(tokens)
    if doubled:
        result.extend(doubled)

    single = parse_quotation(
        tokens,
        start_tag=konrad.Mark.QUOTATION_MARK_SINGLE_OPEN,
        end_tag=konrad.Mark.QUOTATION_MARK_SINGLE_CLOSE,
    )
    if single:
        result.extend(single)
    return result


def parse_quotation(
    tokens,
    start_tag=konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    end_tag=konrad.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
):
    result = []
    start, end = None, None
    # TODO: EXTEND THIS
    for index, item in enumerate(tokens):
        if start is None and end is None:
            if item == end_tag:
                result.append((None, index))
                continue
            if item == start_tag:
                start = index
                continue
        elif start is not None:
            if item == end_tag:
                result.append((start, index + 1))
                start = None
                continue
        elif end is not None:
            pass
    return result


REVERSED = {value: key for key, value in konrad.mark.MATCH.items()}


def mark2str(item) -> str:
    with contextlib.suppress(KeyError):
        item = REVERSED[item]
    return item


def raw_quotation(tokens, indexes) -> list:
    result = []
    for start, end in indexes:
        collected = [mark2str(tokens[index]) for index in range(start, end)]
        result.append(' '.join(collected))
    return result
