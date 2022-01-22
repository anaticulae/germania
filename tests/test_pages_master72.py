# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import german


def test_text_seventytwo_extract_sentences():
    expected = firstpage_sentences()
    raw = ' '.join(expected)
    splitted = german.sentence_tokenize(raw)
    assert len(splitted) == len(expected)
    assert splitted == expected


SEVENTYTWO_FIRSTPAGE = os.path.join(
    german.ROOT,
    'tests/text/seventytwo_firstpage.txt',
)


def firstpage_sentences():
    assert os.path.exists(SEVENTYTWO_FIRSTPAGE), SEVENTYTWO_FIRSTPAGE

    content = utila.file_read(SEVENTYTWO_FIRSTPAGE)
    splitted = content.split(utila.NEWLINE * 2)

    sentences = [item.replace(utila.NEWLINE, ' ').strip() for item in splitted]
    return sentences
