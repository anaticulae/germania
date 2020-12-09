# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad

import german
import tests.test_words_split

SENTENCE = german.split_sentences(tests.test_words_split.SENTENCE)[0]


def test_sequence_match_double_pattern():
    """Validate multiple pattern and avoid duplicated results."""
    expected = [
        (
            konrad.Mark.BRACKET_OPEN,
            'siehe',
            'Abb.',
            german.WordType.NUMBER,
            konrad.Mark.BRACKET_CLOSE,
        ),
        '(siehe Abb. 1)',  # duplicated pattern
    ]
    searched = german.searches(expected, SENTENCE)
    collected = [(31, 36)]
    assert searched == collected


def test_sequence_match_simple_pattern_tokenscomplex():
    expected = [
        '(siehe Abb. 1000)',
    ]
    searched = german.searches(expected, SENTENCE)
    collected = [(31, 36)]
    assert searched == collected


def test_sequence_match_simple_pattern_not_complex():
    expected = [
        '(siehe Abb. 1000)',
    ]
    searched = german.searches(expected, SENTENCE, tokens_complex=False)
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
    searched = german.searches(pattern, sentence, comparecontent=False)
    expected = [(2, 6)]
    assert expected == searched
