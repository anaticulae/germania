# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import germania.improve.abbreviation
import germania.improve.highnote
import germania.improve.href

TODO = (
    germania.improve.abbreviation.abbreviation_magic,
    germania.improve.highnote.highnote_magic,
    germania.improve.href.href_magic,
)


@utila.cacheme
def text_magic(text: str) -> str:
    for pattern in TODO:
        text = pattern(text)
    return text
