# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import german.improve.abbreviation
import german.improve.highnote
import german.improve.href

TODO = (
    german.improve.abbreviation.abbreviation_magic,
    german.improve.highnote.highnote_magic,
    german.improve.href.href_magic,
)


@utila.cacheme
def text_magic(text: str) -> str:
    for pattern in TODO:
        text = pattern(text)
    return text
