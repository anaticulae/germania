# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import nltk

from tests.test_language import MIXED


def test_tokenize_words():
    tokens = list(nltk.word_tokenize(MIXED, language='german'))
    assert len(tokens) == 105


def test_tokenize_sentence():
    sentences = list(nltk.sent_tokenize(MIXED, language='german'))
    assert len(sentences) == 4
