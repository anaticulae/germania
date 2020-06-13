# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utila


def hyperlink(raw: str):
    r"""\
    >>> hyperlink('Before: http://student.unifr.ch/\nReferenzrahmen2001.pdf after.')[0]
    'http://student.unifr.ch/Referenzrahmen2001.pdf'
    >>> hyperlink('This is a link:https://www.youtube.com/watch?v=RXbcAYxuZxw')[0]
    'https://www.youtube.com/watch?v=RXbcAYxuZxw'
    >>> hyperlink('Text.http://google.de')[0]
    'http://google.de'
    """
    raw = raw.replace('\n', '')
    pattern = r"""
    (http|https|www)[:]//[\w\d\./\-\?\=]+
    """
    result = []
    for item in re.finditer(pattern, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        result.append(matched)
    return result
