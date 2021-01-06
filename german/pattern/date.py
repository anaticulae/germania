# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator
import re

import utila


def years(raw: str, min_=1950, max_=2020):
    """Extract sorted list of years out of `raw` text.

    >>> years('1999, Helm was born in 1987. Mud exists since 1800. 2050 20000 2020')
    [1987, 1999, 2020]
    """
    result = []
    pattern = r'\b(19|20)\d{2}\b'
    for item in re.finditer(pattern, raw):
        item = utila.extract_match(item)
        year = int(item)
        if min_ <= year <= max_:
            result.append(year)
    result = sorted(result)
    return result


def dates(raw: str, min_year=1950, max_year=2020):
    """Extract sorted list of dates out of `raw` text.

    >>> dates('Stand 20.10.2020, (15.11.2014), 01.01.1999 01.01.1940')
    [(1999, 1, 1), (2014, 11, 15), (2020, 10, 20)]
    """
    result = []
    pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
    for item in re.findall(pattern, raw):
        day, month, year = item
        day, month, year = int(day), int(month), int(year)
        if not 1 <= day <= 31:
            continue
        if not 1 <= month <= 12:
            continue
        if not min_year <= year <= max_year:
            continue
        result.append((year, month, day))
    result = sorted(result, key=operator.itemgetter(0, 1, 2))
    return result
