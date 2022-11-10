# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

# TODO: DO NOT CHANGE HYPERLINK
# TODO: MOVE TO A MORE GENERAL PLACE
TABLE = str.maketrans({'∼': '~'})

CHARS = r'[\w\d\./\-\_\?\=\&\%\+\~\#]+[\w\d/\?\=\&\%]'
HYPERLINK = utila.compiles(rf"""
    (
        (https://|http://|www\.)
        {CHARS}+
        [\w\d/\?\=\&\%]                     # no dot at the end
    |
        [\w\d\-\_\.]+?                      # soft pattern without url start
        \.
        (de|net|org|com|co\.uk|\w{2,3})
        [\/\#]
        {CHARS}
    )
""")


@utila.cacheme
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
    >>> hyperlink('https://news.linkedin.com/about-us#Statistics')
    ['https://news.linkedin.com/about-us#Statistics']
    >>> hyperlink('https://news.linkedin.com/#Statistics')
    ['https://news.linkedin.com/#Statistics']
    """
    raw = raw.replace('\n', '')
    raw = raw.translate(TABLE)
    # TODO: REPLACE THIS PATTERN
    result = []
    for item in HYPERLINK.finditer(raw):
        value = prepare(
            item,
            position=position,
            verbose=verbose,
        )
        result.append(value)
    return result


LOCALLINK = utila.compiles(r"""
    (
        file[:]
        [\/]{2,3}
        [cdef]                                  # windows local drive
        [:]
        (
            [\w\d\./\-\_\?\=\&\%\+\~]+
            [\w\d/\?\=\&\%]                     # no dot at the end
        )
    )
""")


def locallink(raw: str, position: bool = False, verbose: bool = False) -> list:
    """\
    >>> locallink('Hier liegt das document: file:///C:/kiwi/bachelor028.pdf.')
    ['file:///C:/kiwi/bachelor028.pdf']
    >>> locallink('vom 21.06.2016, unter: file:///C:/Users/user/Downloads/MEMO-16-2265_DE.pdf ', position=True)
    [('file:///C:/Users/user/Downloads/MEMO-16-2265_DE.pdf', 23)]
    """
    raw = raw.replace('\n', '')
    result = []
    for item in LOCALLINK.finditer(raw):
        value = prepare(
            item,
            position=position,
            verbose=verbose,
        )
        result.append(value)
    return result


def links(raw: str, position: bool = False, verbose: bool = False) -> list:
    """\
    >>> links('Available: wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021'
    ... 'document: file:///C:/kiwi/bachelor028.pdf.',
    ... verbose=True, position=True)
    [(('wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021document', 11)...(('file:///C:/kiwi/bachelor028.pdf', 64)...)]
    """
    result = hyperlink(raw, position=position, verbose=verbose)
    if localrefs := locallink(raw, position=position, verbose=verbose):
        # avoid side effects localrefs must not change result of hyperlink
        result = result + localrefs
    if position:
        result.sort(key=lambda x: x[0][1] if verbose else x[1])
    return result


def prepare(item, position: bool = False, verbose: bool = False):
    matched = utila.extract_match(item)
    value = matched
    if position:
        value = (value, item.span()[0])
    if verbose:
        value = (value, matched)
    return value
