# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import tests.test_sentence_split


def test_quotation_extract():
    first, second = german.split_sentences(tests.test_sentence_split.STANDARD)  # pylint:disable=W0632
    expected = [
        (0, 3),
        (9, 14),
    ]
    first_quotes = german.extract_quotes(first)
    assert first_quotes == expected

    expected = [
        (4, 7),
    ]
    second_quotes = german.extract_quotes(second)
    assert second_quotes == expected


def test_quotation_raw():
    first, second = german.split_sentences(tests.test_sentence_split.STANDARD)  # pylint:disable=W0632
    expected = [
        (0, 3),
        (9, 14),
    ]
    splitted = german.split_words(first)
    raw = german.raw_quotation(splitted, expected)
    assert len(raw) == 2

    expected = [
        (4, 7),
    ]
    splitted = german.split_words(second)
    raw = german.raw_quotation(splitted, expected)
    assert len(raw) == 1
