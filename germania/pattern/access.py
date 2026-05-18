# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Reference
=========

accessed
--------

>>> accessed('[Online; Zugriff Oktober 20, 2015]')
[((2015, 10, 20), 'Online; Zugriff Oktober 20, 2015')]
>>> accessed('Version:August 2012')
[((2012, 8, 0), 'Version:August 2012')]
>>> accessed('Zugriff am 19.06.2014')
[((2014, 6, 19), 'Zugriff am 19.06.2014')]
>>> assert not accessed('Juli')  # regression
"""

import contextlib

import utila

import germania.utils.month

MONTHREGEX = germania.utils.month.MONTH_REGEX

MONTHDAYYEAR = r'[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<day>\d{1,2})\,[ ]{0,3}(?P<year>\d{2,4})'
DAYMONTHYEAR = r'[ ]{0,3}(?P<day>\d{1,2})[ ]{0,2}[\.\-][ ]{0,2}(?P<month>\d{1,2})[ ]{0,2}[\.\-][ ]{0,2}(?P<year>\d{2,4})'
DAYTMONTHYEAR = r'[ ]{0,3}(?P<day>\d{1,2})\.[ ]{0,3}(?P<month>' + MONTHREGEX + r')[ ]{0,3}(?P<year>\d{2,4})'
YEARMONTHDAY = r'[ ]{0,3}(?P<year>\d{2,4})[ ]{0,2}[\.\-][ ]{0,2}(?P<month>\d{1,2})[ ]{0,2}[\.\-][ ]{0,2}(?P<day>\d{1,2})'

SIMPLE = r"""
    \(?
    (
        (Online\;?|Letzter)[ ]{0,3}Zugriff[ ]{0,3}\:?|
        Zugriff[ ]{0,3}(am)?|
        Datum[ ]des[ ]{0,3}Zugriffs?[ ]{0,3}(am)?\:?|
        Abgerufen[ ]{0,3}(am[ ]{0,3})?|
        Accessed[ ]{0,3}(on[ ]{0,3})?|
        Stand:[ ]{0,3}
    )
    %s
    \)?
"""

PATTERN = [
    SIMPLE % DAYMONTHYEAR,
    SIMPLE % DAYTMONTHYEAR,
    SIMPLE % MONTHDAYYEAR,
    SIMPLE % YEARMONTHDAY,
    r'Version\:?[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<year>\d{2,4})',
]
PATTERN = [utila.compiles(pattern) for pattern in PATTERN]


@utila.cacheme
def accessed(text: str, verbose: bool = True):
    """\
    >>> accessed('[Letzter Zugriff: 16.02.15]')
    [((15, 2, 16), 'Letzter Zugriff: 16.02.15')]
    >>> accessed('(Datum des Zugriffs: 05. Juli 2004)')
    [((2004, 7, 5), '(Datum des Zugriffs: 05. Juli 2004)')]
    >>> accessed('Abgerufen am 06.06.2015')
    [((2015, 6, 6), 'Abgerufen am 06.06.2015')]
    >>> accessed('Abgerufen am 2015.06.06', verbose=False)
    [(2015, 6, 6)]
    >>> accessed('(Stand: 15.7.2014).')
    [((2014, 7, 15), '(Stand: 15.7.2014)')]
    >>> accessed('Accessed on 2020- 08-09')
    [((2020, 8, 9), 'Accessed on 2020- 08-09')]
    """
    result = []
    for pattern in PATTERN:
        for matched in pattern.finditer(text):
            raw = utila.extract_match(matched)
            text = utila.ghost_replace(text, pattern=raw)
            date = (
                int(matched['year']),
                germania.utils.month.month(matched['month']),
                day(matched),
            )
            if verbose:
                result.append((date, raw))
            else:
                result.append(date)
    return result


def day(matched):
    with contextlib.suppress(IndexError):
        return int(matched['day'])
    return 0
