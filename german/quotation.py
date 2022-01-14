# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import functools

import knlp
import konrad
import konrad.mark
import utila

DOUBLE_SIMPLE = (
    konrad.Mark.QUOTATION_MARK,
    konrad.Mark.QUOTATION_MARK,
)
DOUBLE_GER = (
    konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    konrad.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
)
DOUBLE_ENG = (
    konrad.Mark.EN_QUOTATION_MARK_DOUBLE_OPEN,
    konrad.Mark.EN_QUOTATION_MARK_DOUBLE_CLOSE,
)
SINGLE_GER = (
    konrad.Mark.QUOTATION_MARK_SINGLE_OPEN,
    konrad.Mark.QUOTATION_MARK_SINGLE_CLOSE,
)
SINGLE_ENG = (
    konrad.Mark.EN_QUOTATION_MARK_SINGLE_OPEN,
    konrad.Mark.EN_QUOTATION_MARK_SINGLE_CLOSE,
)


@functools.lru_cache(maxsize=4096)
def extract_quotes(items: str, lang='science') -> list:  # pylint:disable=W0613
    assert isinstance(items, str), type(items)
    # prepare token
    tokens = knlp.word_tokenize(items, language=lang)
    tokens = [konrad.matchesmore(word, lang=lang) for word in tokens]
    # start parsing
    result = []
    for signs in (
            DOUBLE_ENG if lang == konrad.ENGLISH else DOUBLE_GER,
            SINGLE_ENG if lang == konrad.ENGLISH else SINGLE_GER,
            DOUBLE_SIMPLE,
    ):
        parsed = parse_quotation(tokens, *signs)
        if not parsed:
            continue
        result.extend(parsed)
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
            elif item == start_tag:
                start = index
            continue
        if start is not None:
            if item == end_tag:
                result.append((start, index + 1))
                start = None
        # if end is not None:
        #     pass
    return result


REVERSED = {value: key for key, value in konrad.mark.MATCH.items()}


@functools.lru_cache(maxsize=4096)
def mark2str(item) -> str:
    with contextlib.suppress(KeyError):
        item = REVERSED[item]
    return item


def raw_quotation(tokens, indexes) -> list:
    result = []
    for start, end in indexes:
        if end > len(tokens):
            utila.error(f'outranges quotation: {start} {end}')
        # do not out range tokens
        end = min(end, len(tokens))
        collected = [mark2str(tokens[index]) for index in range(start, end)]
        result.append(' '.join(collected))
    return result
