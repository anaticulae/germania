# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilo

import germania
import tests


@pytest.mark.xfail(reason='make it run')
def test_text_seventytwo_extract_sentences():
    expected = firstpage_sentences()
    raw = ' '.join(expected)
    splitted = germania.sentence_tokenize(raw)
    tests.assert_length(splitted, len(expected))
    assert splitted == expected


SEVENTYTWO_FIRSTPAGE = os.path.join(
    germania.ROOT,
    'tests/text/seventytwo_firstpage.txt',
)


def firstpage_sentences():
    assert os.path.exists(SEVENTYTWO_FIRSTPAGE), SEVENTYTWO_FIRSTPAGE

    content = utilo.file_read(SEVENTYTWO_FIRSTPAGE)
    splitted = content.split(utilo.NEWLINE * 2)

    sentences = [item.replace(utilo.NEWLINE, ' ').strip() for item in splitted]
    return sentences
