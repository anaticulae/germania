# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import konradus
import konradus.mark
import utilo

import germania

DOUBLE_SIMPLE = (
    konradus.Mark.QUOTATION_MARK,
    konradus.Mark.QUOTATION_MARK,
)
DOUBLE_GER = (
    konradus.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    konradus.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
)
DOUBLE_ENG = (
    konradus.Mark.EN_QUOTATION_MARK_DOUBLE_OPEN,
    konradus.Mark.EN_QUOTATION_MARK_DOUBLE_CLOSE,
)
SINGLE_GER = (
    konradus.Mark.QUOTATION_MARK_SINGLE_OPEN,
    konradus.Mark.QUOTATION_MARK_SINGLE_CLOSE,
)
SINGLE_ENG = (
    konradus.Mark.EN_QUOTATION_MARK_SINGLE_OPEN,
    konradus.Mark.EN_QUOTATION_MARK_SINGLE_CLOSE,
)


@utilo.cacheme
def extract_quotes(items: str, lang='science') -> list:  # pylint:disable=W0613
    assert isinstance(items, str), type(items)
    # prepare token
    tokens = germania.word_tokenize(
        items,
        lang=lang,
        validate_sentences=False,
    )
    tokens = [konradus.matchesmore(word, lang=lang) for word in tokens]
    # start parsing
    result = []
    for signs in (
            DOUBLE_ENG if lang == konradus.ENGLISH else DOUBLE_GER,
            SINGLE_ENG if lang == konradus.ENGLISH else SINGLE_GER,
            DOUBLE_SIMPLE,
    ):
        parsed = parse_quotation(tokens, *signs)
        if not parsed:
            continue
        result.extend(parsed)
    return result


def parse_quotation(
    tokens,
    start_tag=konradus.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    end_tag=konradus.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
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


REVERSED = {value: key for key, value in konradus.mark.MATCH.items()}


@utilo.cacheme
def mark2str(item) -> str:
    with contextlib.suppress(KeyError):
        item = REVERSED[item]
    return item


def raw_quotation(tokens, indexes) -> list:
    result = []
    for start, end in indexes:
        if end > len(tokens):
            utilo.error(f'outranges quotation: {start} {end}')
        # do not out range tokens
        end = min(end, len(tokens))
        collected = [mark2str(tokens[index]) for index in range(start, end)]
        result.append(' '.join(collected))
    return result
