# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Reference
=========

accessed
--------

>>> accessed('[Online; Zugriff Oktober 20, 2015]')
((2015, 10, 20), 'Online; Zugriff Oktober 20, 2015')
>>> accessed('Version:August 2012')
((2012, 8, 0), 'Version:August 2012')
>>> accessed('Zugriff am 19.06.2014')
((2014, 6, 19), 'Zugriff am 19.06.2014')
>>> assert accessed('Juli') is None  # regression
"""

import contextlib
import functools

import utila

import german.utils.month

MONTHREGEX = german.utils.month.MONTH_REGEX

MONTHDAYYEAR = r'[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<day>\d{1,2})\,[ ]{0,3}(?P<year>\d{2,4})'
DAYMONTHYEAR = r'[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})'
DAYTMONTHYEAR = r'[ ]{0,3}(?P<day>\d{1,2})\.[ ]{0,3}(?P<month>' + MONTHREGEX + r')[ ]{0,3}(?P<year>\d{2,4})'
YEARMONTHDAY = r'[ ]{0,3}(?P<year>\d{2,4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})'

PATTERN = [
    r'(Online\;?|Letzter)[ ]{0,3}Zugriff\:?' + DAYMONTHYEAR,
    r'(Online\;?|Letzter)[ ]{0,3}Zugriff\:?' + DAYTMONTHYEAR,
    r'(Online\;?|Letzter)[ ]{0,3}Zugriff\:?' + MONTHDAYYEAR,
    r'Version\:?[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<year>\d{2,4})',
    r'Zugriff[ ]{0,3}(am)?' + DAYMONTHYEAR,
    r'Zugriff[ ]{0,3}(am)?' + DAYTMONTHYEAR,
    r'Zugriff[ ]{0,3}(am)?' + MONTHDAYYEAR,
    r'Zugriffs?[ ]{0,3}:?' + DAYTMONTHYEAR,
    r'Abgerufen[ ]{0,3}(am[ ]{0,3})?' + DAYMONTHYEAR,
    r'Abgerufen[ ]{0,3}(am[ ]{0,3})?' + DAYTMONTHYEAR,
    r'Abgerufen[ ]{0,3}(am[ ]{0,3})?' + YEARMONTHDAY,
    DAYMONTHYEAR,
    DAYTMONTHYEAR,
    YEARMONTHDAY,
]


@functools.lru_cache(maxsize=4096)
def accessed(raw: str, verbose: bool = True):
    """\
    >>> accessed('europaeischegemeinschaften?p=all (27.05.2018).')
    ((2018, 5, 27), '27.05.2018')
    >>> accessed('[Letzter Zugriff: 16.02.15]')
    ((15, 2, 16), 'Letzter Zugriff: 16.02.15')
    >>> accessed('(Datum des Zugriffs: 05. Juli 2004)')
    ((2004, 7, 5), 'Zugriffs: 05. Juli 2004')
    >>> accessed('Abgerufen am 06.06.2015')
    ((2015, 6, 6), 'Abgerufen am 06.06.2015')
    >>> accessed('Abgerufen am 2015.06.06', verbose=False)
    (2015, 6, 6)
    """
    for item in PATTERN:
        matched = utila.search(item, raw)
        if not matched:
            continue
        raw = utila.extract_match(matched)
        date = (
            int(matched['year']),
            german.utils.month.month(matched['month']),
            day(matched),
        )
        if verbose:
            return (date, raw)
        return date
    return None


def day(matched):
    with contextlib.suppress(IndexError):
        return int(matched['day'])
    return 0
