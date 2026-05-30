# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import germania.utils.month

YEARS = utilo.compiles(r'\b(19|20)\d{2}\b')
MONTH_REGEX = germania.utils.month.MONTH_REGEX


@utilo.cacheme
def years(raw: str, min_=1950, max_=2025, verbose: bool = False):
    """Extract sorted list of years out of `raw` text.

    >>> years('1999, Helm was born in 1987. Mud exists since 1800. 2050 20000 2020')
    [1987, 1999, 2020]
    >>> years('Helm was born in 1987.', verbose=True)
    [(1987, '1987')]
    """
    result = []
    for item in YEARS.finditer(raw):
        year = int(item[0])
        if min_ <= year <= max_:
            parsed = year
            if verbose:
                parsed = (year, item[0])
            result.append(parsed)
    result = sorted(result, key=lambda x: x[0] if verbose else x)
    return result


DATES = utilo.compiles(r"""
    (
        \d{4}|
        \d{1,2})\.(\d{1,2})\.(\d{4}|
        \d{1,2}
    )
""")


def dates_master(
    raw: str,
    year_min=1950,
    year_max=2025,
    verbose: bool = False,
    sort: bool = True,
):  # pylint:disable=W0613
    """\
    >>> dates_master('Aug. 1991')
    [('1991', 8, 0)]
    >>> dates_master('Stand 20.10.2020', verbose=True)
    [((2020, 10, 20), '20.10.2020')]
    """
    result = []
    for method in (
            dates_month_year,
            dates,
    ):
        parsed = method(raw, sort=sort, verbose=True)
        if not parsed:
            continue
        for item in parsed:
            raw = raw.replace(item[1], '*' * len(item[1]))
            result.append(item)
    # sort result by first occurence
    result = sorted(result, key=lambda x: raw.find(x[1]))
    if not verbose:
        result = [item[0] for item in result]
    if sort:
        result = sortby_year(result, verbose=verbose)
    return result


@utilo.rename(min_year='year_min', max_year='year_max')
@utilo.cacheme
def dates(
    raw: str,
    year_min=1950,
    year_max=2025,
    verbose: bool = False,
    sort: bool = True,
):
    """Extract sorted list of dates out of `raw` text.

    >>> dates('Stand 20.10.2020, (15.11.2014), 01.01.1999 01.01.1940')
    [(1999, 1, 1), (2014, 11, 15), (2020, 10, 20)]
    >>> dates('Stand 20.10.2020', verbose=True)
    [((2020, 10, 20), '20.10.2020')]
    >>> dates('Stand 2021.09.10', verbose=True)
    [((2021, 9, 10), '2021.09.10')]
    >>> dates('europaeischegemeinschaften?p=all (27.05.2018).', verbose=True)
    [((2018, 5, 27), '27.05.2018')]
    """
    result = []
    for item in DATES.finditer(raw):
        day, month, year = item[1], item[2], item[3]
        day, month, year = int(day), int(month), int(year)
        if day > year:
            year, day = day, year
        if not 1 <= day <= 31:
            continue
        if not 1 <= month <= 12:
            continue
        if not year_min <= year <= year_max:
            continue
        parsed = (year, month, day)
        if verbose:
            parsed = (parsed, item[0])
        result.append(parsed)
    if sort:
        result = sortby_year(result, verbose=verbose)
    return result


MONTH_YEAR = utilo.compiles(MONTH_REGEX + r'[ ]{0,3}(\d{2,4})')


def dates_month_year(raw: str, verbose: bool = True, sort: bool = True):
    """\
    >>> dates_month_year('Aug. 1991')
    [(('1991', 8, 0), 'Aug. 1991')]
    """
    result = []
    for item in MONTH_YEAR.finditer(raw):
        month, year, day = item[1], item[2], 0
        month = germania.utils.month.month(month)
        parsed = (year, month, day)
        if verbose:
            parsed = (parsed, item[0])
        result.append(parsed)
    if sort:
        result = sortby_year(result, verbose=verbose)
    return result


def sortby_year(items, verbose: bool = True):
    # sort by year, month, day
    for pos in range(3):
        items = sorted(
            items,
            key=lambda x: x[0][pos] if verbose else x[pos],  # pylint:disable=W0640
        )
    return items
