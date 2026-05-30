# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utilo

PATTERN = r"""
[\.\w\-\_]+@[\w\.\-\_]+
"""


@utilo.cacheme
def mails(raw: str) -> list:
    """\
    >>> mails('This is email:1helmut.k.fahrendholz@mailbox.tu-berlin.de end.')
    ['1helmut.k.fahrendholz@mailbox.tu-berlin.de']
    """
    result = []
    for item in re.finditer(PATTERN, raw, flags=re.VERBOSE):
        matched = utilo.extract_match(item)
        result.append(matched)
    return result
