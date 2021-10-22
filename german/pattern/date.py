# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import re

YEARS = re.compile(r'\b(19|20)\d{2}\b')


@functools.lru_cache(maxsize=4096)
def years(raw: str, min_=1950, max_=2020, verbose: bool = False):
    """Extract sorted list of years out of `raw` text.

    >>> years('1999, Helm was born in 1987. Mud exists since 1800. 2050 20000 2020')
    [1987, 1999, 2020]
    >>> years('Helm was born in 1987.', verbose=True)
    [(1987, '1987')]
    """
    result = []
    for item in re.finditer(YEARS, raw):
        year = int(item[0])
        if min_ <= year <= max_:
            parsed = year
            if verbose:
                parsed = (year, item[0])
            result.append(parsed)
    result = sorted(result, key=lambda x: x[0] if verbose else x)
    return result


DATES = re.compile(r'(\d{1,2})\.(\d{1,2})\.(\d{4})')


@functools.lru_cache(maxsize=4096)
def dates(raw: str, min_year=1950, max_year=2020, verbose: bool = False):
    """Extract sorted list of dates out of `raw` text.

    >>> dates('Stand 20.10.2020, (15.11.2014), 01.01.1999 01.01.1940')
    [(1999, 1, 1), (2014, 11, 15), (2020, 10, 20)]
    >>> dates('Stand 20.10.2020', verbose=True)
    [((2020, 10, 20), '20.10.2020')]
    """
    result = []
    for item in re.finditer(DATES, raw):
        day, month, year = item[1], item[2], item[3]
        day, month, year = int(day), int(month), int(year)
        if not 1 <= day <= 31:
            continue
        if not 1 <= month <= 12:
            continue
        if not min_year <= year <= max_year:
            continue
        parsed = (year, month, day)
        if verbose:
            parsed = (parsed, item[0])
        result.append(parsed)
    # sort by year, month, day
    for pos in range(3):
        result = sorted(result, key=lambda x: x[0][pos] if verbose else x[pos])  # pylint:disable=W0640
    return result
