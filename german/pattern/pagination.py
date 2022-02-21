# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
import functools
import re

import utila

PAGENUMBERS = utila.compiles(r"""
    \b
    (S|S\.|Seite|p|p\.|page)
    [ ]{0,4}
    (
        (?P<pstart>\d{1,4})[ ]{0,2}(-|–)[ ]{0,2}(?P<pend>\d{1,4})|
        (?P<page>\d{1,4})
    )
""")


@functools.lru_cache(maxsize=4096)
def pagenumbers(raw: str, verbose: bool = False):
    """Extract single pages and page ranges out of `raw` text.

    >>> pagenumbers('S. 13-50 S.30 S. 1-5 S.319-350, Seite 20–30., page 500 p.4')
    [(1, 5), (4, 4), (13, 50), (20, 30), (30, 30), (319, 350), (500, 500)]
    >>> pagenumbers('S. 13-50', verbose=True)
    [((13, 50), 'S. 13-50')]
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


@functools.lru_cache(maxsize=4096)
def pages(raw: str):
    """\
    >>> pages('IEEE Joint, 2004, S. 113-117')
    ('S. 113-117', (113, 117))
    >>> pages('p.103')
    ('p.103', (103,))
    >>> pages('text before, S. 263–268')
    ('S. 263–268', (263, 268))
    """
    pattern = r"""(
         (Seite|S\.|p\.|P\.|page)[ ]{0,3}
         (
          (?P<pagestart>\d{1,4})[ ]{0,3}(\-|–)[ ]{0,3}(?P<pageend>\d{1,4})|
          (?P<page>\d{1,4})
         )
    )
    """
    matched = re.search(pattern, raw, re.VERBOSE)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['page']),)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['pagestart']), int(matched['pageend']))
    return None


COMPLEX = utila.compiles(r"""
(
    (\,){0,1}[ ]{0,3}
    (
        (?P<pagestart>\d{1,4})[ ]{0,3}(\-|–)[ ]{0,3}(?P<pageend>\d{1,4})(\.|$)
    )
)
""")


@functools.lru_cache(maxsize=4096)
def pages_complex(raw: str):
    """\
    >>> pages_complex('Germaniques 53, H. 2, 93-122.')
    (', 93-122.', (93, 122))
    >>> pages_complex('Blutalkohol, 41, 1-10.')
    (', 1-10.', (1, 10))
    >>> pages_complex(',41, 1-10')
    (', 1-10', (1, 10))
    """
    matched = COMPLEX.search(raw)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    with contextlib.suppress(TypeError):
        start = int(matched['pagestart'])
        end = int(matched['pageend'])
        return raw, (start, end)
    return None
