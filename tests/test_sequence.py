# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konradus

import germania
import tests.test_words_split

SENTENCE = germania.sentence_tokenize(tests.test_words_split.SENTENCE)[0]


def test_sequence_match_double_pattern():
    """Validate multiple pattern and avoid duplicated results."""
    expected = [
        (
            konradus.Mark.BRACKET_OPEN,
            'siehe',
            'Abb.',
            germania.WordType.NUMBER,
            konradus.Mark.BRACKET_CLOSE,
        ),
        '(siehe Abb. 1)',  # duplicated pattern
    ]
    searched = germania.searches(expected, SENTENCE)
    collected = [(31, 36)]
    assert searched == collected


def test_sequence_match_simple_pattern_tokens_complex():
    expected = [
        '(siehe Abb. 1000)',
    ]
    searched = germania.searches(expected, SENTENCE)
    collected = [(31, 36)]
    assert searched == collected


def test_sequence_match_simple_pattern_not_complex():
    expected = [
        '(siehe Abb. 1000)',
    ]
    searched = germania.searches(expected, SENTENCE, tokens_complex=False)
    assert not searched


def test_search_braket_sequence():
    pattern = (
        '[Ka14]',
        '[Mag13]',
        '[Hof11, S. 314f]',
        '[Hof11, S. 309-311]',
        '[RNB12, S. 62ff]',
    )
    sentence = 'Zum Arbeitsschutzproblm [EB03].'
    searched = germania.searches(pattern, sentence, compare_content=False)
    expected = [(2, 6)]
    assert expected == searched
