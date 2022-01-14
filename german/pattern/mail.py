# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import re

import utila

PATTERN = r"""
[\.\w\-\_]+@[\w\.\-\_]+
"""


@functools.lru_cache(maxsize=4096)
def mails(raw: str) -> list:
    """\
    >>> mails('This is email:1helmut.k.fahrendholz@mailbox.tu-berlin.de end.')
    ['1helmut.k.fahrendholz@mailbox.tu-berlin.de']
    """
    result = []
    for item in re.finditer(PATTERN, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        result.append(matched)
    return result
