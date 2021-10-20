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
('[Online; Zugriff Oktober 20, 2015]', (2015, 10, 20))
>>> accessed('Version:August 2012')
('Version:August 2012', (2012, 8, 0))
>>> accessed('Zugriff am 19.06.2014')
('Zugriff am 19.06.2014', (2014, 6, 19))
>>> assert accessed('Juli') is None  # regression
"""

import contextlib
import functools
import re

import utila

import german.utils.month

MONTHREGEX = german.utils.month.MONTH_REGEX


@functools.lru_cache(maxsize=4096)
def accessed(raw: str):
    """\
    >>> accessed('europaeischegemeinschaften?p=all (27.05.2018).')
    ('(27.05.2018)', (2018, 5, 27))
    >>> accessed('[Letzter Zugriff: 16.02.15]')
    ('[Letzter Zugriff: 16.02.15]', (15, 2, 16))
    >>> accessed('(Datum des Zugriffs: 05. Juli 2004)')
    ('Zugriffs: 05. Juli 2004', (2004, 7, 5))
    """
    # yapf:disable
    pattern = [
        r'\[Letzter[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\]',
        r'Letzter[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})',
        r'\[Online[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\]',
        r'\[Online\;[ ]{0,3}Zugriff[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<day>\d{1,2})\,[ ]{0,3}(?P<year>\d{2,4})\]',
        r'Version\:[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<year>\d{2,4})',
        r'Zugriff[ ]{0,3}am[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})',
        r'Zugriffs?[ ]{0,3}:?[ ]{0,3}(?P<day>\d{1,2})\.[ ]{0,3}(?P<month>' + MONTHREGEX + r')[ ]{0,3}(?P<year>\d{2,4})',
        r'\((?P<year>\d{2,4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})\)',
        r'\((?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\)',
        r'\((?P<day>\d{1,2})\.[ ]{0,3}(?P<month>' + MONTHREGEX + r')[ ]{0,3}(?P<year>\d{2,4})\)',
    ]
    # yapf:enable
    for item in pattern:
        matched = re.search(item, raw, re.IGNORECASE | re.VERBOSE)
        if not matched:
            continue
        raw = utila.extract_match(matched)
        date = (
            int(matched['year']),
            german.utils.month.month(matched['month']),
            day(matched),
        )
        return (raw, date)
    return None


def day(matched):
    with contextlib.suppress(IndexError):
        return int(matched['day'])
    return 0
