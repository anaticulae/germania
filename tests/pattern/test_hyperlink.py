# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import german

HYPERLINKS = """\
Before: http://student.unifr.ch/
Referenzrahmen2001.pdf after.
http://student.unifr.ch/Referenzrahmen2001.pdf

This is a link:https://www.youtube.com/watch?v=RXbcAYxuZxw
https://www.youtube.com/watch?v=RXbcAYxuZxw

Text.http://google.de
http://google.de

Gemeinde Neunkirchen 31818\nwww.statistik.at/blickgem/fa1/g31818.pdf (03.12.2017)
www.statistik.at/blickgem/fa1/g31818.pdf

http://www.statistik.at/index.html?includePage=detailedView%C2%A7ionName=Bildung%2C+Kultur&pubId=461
http://www.statistik.at/index.html?includePage=detailedView%C2%A7ionName=Bildung%2C+Kultur&pubId=461

10 Silla and Kaestner from http://www.ppgia.pucpr.br/∼silla/softwares/yasd.zip.
http://www.ppgia.pucpr.br/~silla/softwares/yasd.zip

https://www.menschen_und_gesellschaft/
https://www.menschen_und_gesellschaft/

"""


def prepared():
    result = []
    for index, doubleline in enumerate(HYPERLINKS.split('\n\n')):
        if not doubleline.strip():
            break
        raw, expected = doubleline.rsplit('\n', maxsplit=1)
        raw, expected = raw.strip(), expected.strip()
        expected = expected.split(' ')
        result.append(pytest.param(raw, expected, id=str(index)))
    return result


@pytest.mark.parametrize('raw, expected', prepared())
def test_hyperlinks(raw, expected):
    parsed = german.hyperlink(raw)
    assert parsed == expected


def test_link_cached():
    """As a result of invalid cache multiple parsing produces wrong results."""
    raw = 'file:///C:/kiwi/bachelor028.pdf'
    expected = [raw]
    parsed = german.links(raw)
    assert parsed == expected
    parsed = german.links(raw)
    assert parsed == expected
