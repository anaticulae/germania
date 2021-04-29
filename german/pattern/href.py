# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila

# TODO: MOVE TO A MORE GENERAL PLACE
TABLE = str.maketrans({'∼': '~'})


def hyperlink(raw: str, position: bool = False):
    r"""\
    >>> hyperlink('Before: http://student.unifr.ch/\nReferenzrahmen2001.pdf after.', position=True)
    [('http://student.unifr.ch/Referenzrahmen2001.pdf', 8)]
    """
    raw = raw.replace('\n', '')
    raw = raw.translate(TABLE)
    # TODO: REPLACE THIS PATTERN
    pattern = r"""
    (https://|http://|www\.)
    [\w\d\./\-\?\=\&\%\+\~]+[\w\d/\?\=\&\%]  # no dot at the end
    """
    result = []
    for item in re.finditer(pattern, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        if position:
            result.append((matched, item.span()[0]))
        else:
            result.append(matched)
    return result
