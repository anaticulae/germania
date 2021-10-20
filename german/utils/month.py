# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Month detector
==============

Determine number of month:

>>> import german
>>> german.month('may')
5
"""

import contextlib
import functools

import utila

MONTH_RAW = """\
january
januar
jan

february
februar
feb

märz
marz
march
mar

april
apr

mai
may

juni
june
jun

juli
july
jul

august
aug

september
sep

oktober
october
oct

november
nov

dezember
december
dec
""".strip()

GROUPS = [list(month.splitlines()) for month in MONTH_RAW.split('\n\n')]
MONTH_REGEX = '(' + '|'.join(utila.flatten(GROUPS)) + ')'
MONTH = utila.flatten(GROUPS)


@functools.lru_cache(maxsize=4096)
def month(item: str):
    """\
    >>> month('marz')
    3
    >>> month('kein monat')
    >>> month('02')
    2
    """
    item = item.lower()
    for index, group in enumerate(GROUPS, start=1):
        if item not in group:
            continue
        return index
    with contextlib.suppress(ValueError):
        return int(item)
    return None
