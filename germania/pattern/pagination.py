# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Regression test to avoid parsing `bis 14` as `S 14`
>>> pagenumbers('bis 14.02.2012')
[]
"""
# TODO: UNITE THESE PATTERN LATER

import contextlib

import utilo

PAGES_INTRO = r'(S\.?|Seite|p{1,2}\.?|page)'
PAGES = r"""
    (
        (?P<pstart>\d{1,4})[ ]{0,2}[-–][ ]{0,2}(?P<pend>\d{1,4})|
        (?P<page>\d{1,4})
    )
"""

PAGENUMBERS = utilo.compiles(r"""
    \b
    %s
    [ ]{0,4}
    %s
""" % (PAGES_INTRO, PAGES))


@utilo.cacheme
def pagenumbers(raw: str, verbose: bool = False):
    """Extract single pages and page ranges out of `raw` text.

    >>> pagenumbers('S. 13-50 S.30 S. 1-5 S.319-350, Seite 20–30., page 500 p.4')
    [(1, 5), (4, 4), (13, 50), (20, 30), (30, 30), (319, 350), (500, 500)]
    >>> pagenumbers('S. 13-50', verbose=True)
    [((13, 50), 'S. 13-50')]
    >>> pagenumbers('IEEE. 2013, pp. 595–602.', verbose=True)
    [((595, 602), 'pp. 595–602')]
    >>> pagenumbers('9.Nov (2008), pp. 2579– 2605.')
    [(2579, 2605)]
    """
    result = []
    for item in PAGENUMBERS.finditer(raw):
        try:
            # single page
            pstart = int(item['page'])
            parsed = (pstart, pstart)
            if verbose:
                parsed = (parsed, item[0])
            result.append(parsed)
        except TypeError:
            # from page start till page end
            pstart = int(item['pstart'])
            pend = int(item['pend'])
            parsed = (pstart, pend)
            if verbose:
                parsed = (parsed, item[0])
            result.append(parsed)
    result = sorted(result, key=lambda x: x[0][0] if verbose else x[0])
    return result


PATTERN = utilo.compiles(r"""
(
     %s
     [ ]{0,3}
     %s
)
""" % (PAGES_INTRO, PAGES))


@utilo.cacheme
def page_single(raw: str):
    """\
    >>> page_single('IEEE Joint, 2004, S. 113-117')
    ('S. 113-117', (113, 117))
    >>> page_single('IEEE Joint, 2004, s. 113-117')
    ('s. 113-117', (113, 117))
    >>> page_single('p.103')
    ('p.103', (103,))
    >>> page_single('text before, S. 263–268')
    ('S. 263–268', (263, 268))
    >>> page_single('NO PAGENUMBER') is None
    True
    """
    matched = PATTERN.search(raw)
    if not matched:
        return None
    raw = utilo.extract_match(matched)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['page']),)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['pstart']), int(matched['pend']))
    return None


COMPLEX = utilo.compiles(r"""
(
    (\,){0,1}[ ]{0,3}
    (
        (?P<pstart>\d{1,4})[ ]{0,3}(\-|–)[ ]{0,3}(?P<pend>\d{1,4})(\.|$)
    )
)
""")


@utilo.cacheme
def pages_complex(raw: str):
    """\
    >>> pages_complex('Germaniques 53, H. 2, 93-122.')
    (', 93-122.', (93, 122))
    >>> pages_complex('Blutalkohol, 41, 1-10.')
    (', 1-10.', (1, 10))
    >>> pages_complex(',41, 1-10')
    (', 1-10', (1, 10))
    >>> pages_complex('NO PAGENUMBER') is None
    True
    """
    matched = COMPLEX.search(raw)
    if not matched:
        return None
    raw = utilo.extract_match(matched)
    with contextlib.suppress(TypeError):
        start = int(matched['pstart'])
        end = int(matched['pend'])
        return raw, (start, end)
    return None
