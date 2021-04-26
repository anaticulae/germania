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

PAGE_PATTERN = r"""
    (S|S\.|Seite|p|p\.|page)
    [ ]{0,4}
    (
        (?P<pstart>\d{1,4})[ ]{0,2}(-|–)[ ]{0,2}(?P<pend>\d{1,4})|
        (?P<page>\d{1,4})
    )
"""


def pagenumbers(raw: str):
    """Extract single pages and page ranges out of `raw` text.

    >>> pagenumbers('S. 13-50 S.30 S. 1-5 S.319-350, Seite 20–30., page 500 p.4')
    [(1, 5), (4, 4), (13, 50), (20, 30), (30, 30), (319, 350), (500, 500)]
    """
    result = []
    for item in re.finditer(PAGE_PATTERN, raw, re.VERBOSE | re.IGNORECASE):
        try:
            # single page
            pstart = int(item['page'])
            result.append((pstart, pstart))
        except TypeError:
            # from page start till page end
            pstart = int(item['pstart'])
            pend = int(item['pend'])
            result.append((pstart, pend))
    result = sorted(result, key=operator.itemgetter(0))
    return result
