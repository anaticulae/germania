# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import operator
import re
import typing

import utila

import german


def search(
    pattern: list,
    sentence: list,
    *,
    lowercase: bool = True,
    tokens_complex: bool = True,
    compare_content: bool = True,
) -> list:
    # prepare data
    if isinstance(sentence, str):
        sentence = german.word_tokenize(sentence, validate_sentences=False)
    if isinstance(pattern, re.Pattern):
        return search_regex(
            pattern,
            sentence,
        )
    if isinstance(pattern, str):
        pattern = german.word_tokenize(pattern, validate_sentences=False)
    tokens_length = len(pattern)
    if tokens_length > len(sentence):
        return []
    if lowercase:
        pattern = [lower(item) for item in pattern]
        sentence = [lower(item) for item in sentence]
    sentence = [german.wordtypes(word) for word in sentence]
    if tokens_complex:
        pattern = [german.wordtypes(token) for token in pattern]
    # start searching
    result = []
    for start in range(len(sentence) - len(pattern) + 1):
        selected = sentence[start:start + tokens_length]
        if not _match(
                pattern,
                selected,
                tokens_complex=tokens_complex,
                compare_content=compare_content,
        ):
            continue
        result.append((start, start + tokens_length))
    # Sort findings and remove smaller patterns inside bigger ones
    result = simplify(result)
    return result


def search_regex(
    pattern: re.Pattern,
    sentence: list,
) -> list:
    result = []
    for index, word in enumerate(sentence):
        if not pattern.match(str(word)):
            continue
        result.append((index, index + 1))
    return result


def searches(
    patterns: list,
    sentence: list,
    *,
    lowercase: bool = True,
    tokens_complex: bool = True,
    compare_content: bool = True,
    overlapping_remove: bool = True,
    neighbours_merge: bool = False,
    verbose: bool = False,
) -> list:
    r"""\
    >>> searches([utila.compiles(r'\{\{hn\:\d{1,4}\:nh\}\}')],
    ... 'Treiber charakterisiert.{{hn:7:nh}}', verbose=True)
    ([(3, 4)], [['{{hn:7:nh}}']])
    """
    if neighbours_merge:
        assert overlapping_merge, 'enable overlapping_merge'
    # prepare here to avoid preparing for every tokens
    if isinstance(sentence, str):
        sentence = german.word_tokenize(sentence, validate_sentences=False)
    result = []
    for pattern in patterns:
        matches = search(
            pattern=pattern,
            sentence=sentence,
            lowercase=lowercase,
            tokens_complex=tokens_complex,
            compare_content=compare_content,
        )
        if matches:
            result.extend(matches)
    # TODO: SORT RESULT?
    result = utila.make_unique(result)
    if overlapping_remove:
        result = overlapping_merge(result, connected_merge=neighbours_merge)
    if verbose:
        if not result:
            return []
        raw = [sentence[start:end] for start, end in result]
        return result, raw
    return result


def overlapping_merge(items: list, connected_merge: bool = False) -> list:
    """\
    >>> overlapping_merge([(0, 5), (4, 9)])
    [(0, 5), (4, 9)]
    >>> overlapping_merge([(2, 5), (3, 4)])
    [(2, 5)]
    >>> overlapping_merge([(0, 5), (5, 9)], connected_merge=True)
    [(0, 9)]
    >>> overlapping_merge([(38, 41), (38, 44), (38, 45)])  # 'biggest groups'
    [(38, 45)]
    """
    # sort second value first to move 'biggest groups' to the front
    items = sorted(items, key=lambda x: x[1], reverse=True)
    items = sorted(items, key=lambda x: x[0])
    result = []
    done = set()
    for item in items:
        start, stop = item
        if all((item in done for item in range(start, stop))):
            continue
        for index in range(start, stop):
            done.add(index)
        result.append(item)
    if not result or not connected_merge:
        return result
    # merge connected
    connected = [result[0]]
    for item in result[1:]:
        if connected[-1][1] == item[0]:
            # update last item
            connected[-1] = (connected[-1][0], item[1])
        else:
            connected.append(item)
    return connected


def init(text: str) -> set:
    """Prepare sentence search data."""
    return {item.lower() for item in text.splitlines() if item}


def lower(item: typing.Any) -> typing.Any:
    with contextlib.suppress(AttributeError):
        return item.lower()
    return item


def _match(
    chunk: list,
    expected: list,
    *,
    tokens_complex: bool,
    compare_content: bool,
) -> bool:
    assert len(chunk) == len(expected)
    for item, item_expected in zip(chunk, expected):
        if tokens_complex:
            if item & item_expected:
                # matching items in `item` and `item_expected`. Check next
                # item.
                continue
            if compare_content:
                # str-content is not equal, stop matching sequence
                return False
            # content is not equal, but we only check that data type
            # matches
            item_str = any(isinstance(it, str) for it in item)
            if not item_str:
                return False
            item_expected_str = any(isinstance(it, str) for it in item_expected)
            if not item_expected_str:
                return False
            continue
        if item not in item_expected:
            return False
    return True


def simplify(items: list) -> list:
    """\
    >>> simplify([(15, 20), (15, 25), (14, 15), (1, 3)])
    [(1, 3), (14, 15), (15, 20), (15, 25)]
    >>> simplify([(5, 8), (3, 9)])
    [(3, 9)]
    """
    if not items:
        return []
    items = sorted(items, key=operator.itemgetter(0, 1))
    result = [items[0]]
    for item in items[1:]:
        start, end = result[-1]
        if start <= item[0] <= item[1] <= end:
            continue
        result.append(item)
    return result
