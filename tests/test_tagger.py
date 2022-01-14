# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import nltk

import german
from tests.test_language import SINGLE


def test_tag_example():
    tokens = list(nltk.word_tokenize(SINGLE, language='german'))
    tagged = german.word_tag(tokens)
    assert len(tagged) == 8
    # TODO: IMPROVE CHECK
