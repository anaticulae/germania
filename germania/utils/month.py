# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Month detector
==============

Determine number of month:

>>> import germania
>>> germania.month('may')
5
"""

import contextlib

import utilo

MONTH_RAW = """\
JANUARY
JANUAR
JAN.
JAN

FEBRUARY
FEBRUAR
FEB.
FEB

MÄRZ
MARZ
MARCH
MAR.
MAR

APRIL
APR.
APR

MAI
MAY

JUNI
JUNE
JUN.
JUN

JULI
JULY
JUL.
JUL

AUGUST
AUG.
AUG

SEPTEMBER
SEP.
SEP

OKTOBER
OCTOBER
OCT.
OCT

NOVEMBER
NOV.
NOV

DEZEMBER
DECEMBER
DEC.
DEC
"""

GROUPS = [
    utilo.splitlines(month, unique=False, lowers=False) for month in
    utilo.splitlines(MONTH_RAW, pattern='\n\n', unique=False, lowers=False)
]
MONTH_REGEX = '(' + '|'.join(utilo.flat(GROUPS)) + ')'
MONTH = utilo.flat(GROUPS)


@utilo.cacheme
def month(item: str):
    """\
    >>> month('marz')
    3
    >>> month('kein monat')
    >>> month('02')
    2
    """
    item = item.upper()
    for index, group in enumerate(GROUPS, start=1):
        if item not in group:
            continue
        return index
    with contextlib.suppress(ValueError):
        return int(item)
    return None
