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


def hyperlink(raw: str, position: bool = False):
    r"""\
    >>> hyperlink('Before: http://student.unifr.ch/\nReferenzrahmen2001.pdf after.')[0]
    'http://student.unifr.ch/Referenzrahmen2001.pdf'
    >>> hyperlink('This is a link:https://www.youtube.com/watch?v=RXbcAYxuZxw', True)[0]
    ('https://www.youtube.com/watch?v=RXbcAYxuZxw', 15)
    >>> hyperlink('Text.http://google.de')[0]
    'http://google.de'
    >>> hyperlink('Gemeinde Neunkirchen 31818\nwww.statistik.at/blickgem/fa1/g31818.pdf (03.12.2017')[0]
    'www.statistik.at/blickgem/fa1/g31818.pdf'
    >>> hyperlink('http://www.statistik.at/index.html?includePage=detailedView%C2%A7ionName=Bildung%2C+Kultur&pubId=461')
    ['http://www.statistik.at/index.html?includePage=detailedView%C2%A7ionName=Bildung%2C+Kultur&pubId=461']
    """
    raw = raw.replace('\n', '')
    pattern = r"""
    (http://|https://|www)[\w\d\./\-\?\=\&\%\+]+
    """
    result = []
    for item in re.finditer(pattern, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        if position:
            result.append((matched, item.span()[0]))
        else:
            result.append(matched)
    return result
