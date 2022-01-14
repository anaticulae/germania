# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import re

import utila

# TODO: DO NOT CHANGE HYPERLINK
# TODO: MOVE TO A MORE GENERAL PLACE
TABLE = str.maketrans({'∼': '~'})

CHARS = r'[\w\d\./\-\_\?\=\&\%\+\~]+[\w\d/\?\=\&\%]'
HYPERLINK = rf"""
    (
        (https://|http://|www\.)
        {CHARS}+
        [\w\d/\?\=\&\%]                     # no dot at the end
    |
        [\w\d\-\_\.]+?                      # soft pattern without url start
        \.
        (de|net|org|com|co\.uk|\w{2,3})
        \/
        {CHARS}
    )
"""


@functools.lru_cache(maxsize=4096)
def hyperlink(raw: str, position: bool = False, verbose: bool = False):
    r"""\
    >>> hyperlink('Before: http://student.unifr.ch/\nReferenzrahmen2001.pdf after.', position=True)
    [('http://student.unifr.ch/Referenzrahmen2001.pdf', 8)]
    >>> hyperlink('Wiki [On-line]. Available: wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021')
    ['wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021']
    >>> hyperlink('Wiki [On-line]. Available: wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021', verbose=True)
    [('wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021', 'wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021')]
    >>> hyperlink('persönliche bzw.demographische Daten')
    []
    """
    raw = raw.replace('\n', '')
    raw = raw.translate(TABLE)
    # TODO: REPLACE THIS PATTERN
    result = []
    for item in re.finditer(HYPERLINK, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        value = matched
        if position:
            value = (value, item.span()[0])
        if verbose:
            value = (value, matched)
        result.append(value)
    return result
