# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Examples:
=========

ISBN
----

>>> isbn('Das ist ein Buch ISBN 978-0-9745607-3-1. Bücher sind schön.')
['ISBN 978-0-9745607-3-1']
>>> isbn('ISBN 13: 978-1292-02572-8')
['ISBN 13: 978-1292-02572-8']
>>> isbn('ISBN 978-0-9745607-3-1.')
['ISBN 978-0-9745607-3-1']
>>> isbn('ISBN 0-201-56317-7')
['ISBN 0-201-56317-7']
>>> isbn('ISBN 0-471-22361-1.')
['ISBN 0-471-22361-1']
>>> isbn('ISBN 13: 9781119994398', verbose=True)
[((9781119994398,), 'ISBN 13: 9781119994398')]
>>> isbn('ISBN 3540429883.')
['ISBN 3540429883']
>>> isbn('ISBN: 0521540518')
['ISBN: 0521540518']
>>> isbn('isbn: 978-1-931971-16-4.')
['isbn: 978-1-931971-16-4']
>>> isbn('isbn:1-931666-22-9')
['isbn:1-931666-22-9']

ISSN
----

>>> issn('issn: 0018-9162.')
['issn: 0018-9162']

DOI
---

>>> doi(':DOI:`10.1002/9781119994398`')
[':DOI:`10.1002/9781119994398`']
>>> doi(':DOI:`10.1109/TPAMI.2013.106`')
[':DOI:`10.1109/TPAMI.2013.106`']
>>> doi('DOI: 10.1007/s12532-017-0130-5')
['DOI: 10.1007/s12532-017-0130-5']
>>> doi('DOI:10.1080/10618600.1998.10474789')
['DOI:10.1080/10618600.1998.10474789']
>>> doi('DOI:10.1093/biomet/81.3.425')
['DOI:10.1093/biomet/81.3.425']
>>> doi('DOI:10.2307/1269730')
['DOI:10.2307/1269730']
>>> doi('doi: 10.1145/2723372.2742797.url', verbose=True)
[('doi: 10.1145/2723372.2742797.url', 'doi: 10.1145/2723372.2742797.url')]
"""

import utila

import german

ISBN = utila.compiles(r"""
(
    ISBN\s{0,2}\d{1,2}:|
    ISBN\:?|
)
\s{0,3}
(
    \d{1,3}-\d{1,4}-\d{5,7}-\d{1,3}-\d{1,3}|
    \d{1,3}-\d{1,4}-\d{1,4}-\d{1,4}-\d{1,3}|
    \d{1,3}-\d{1,6}-\d{5,7}-\d{1,3}|
    \d{1,3}-\d{1,6}-\d{1,3}-\d{1,3}|
    \d{10,13}
)
""")


def isbn(raw: str, verbose: bool = False) -> list:
    """\
    >>> isbn('isbn:978-1-4503-2758-9.', verbose=True)
    [((978, 1, 4503, 2758, 9), 'isbn:978-1-4503-2758-9')]
    """
    result = []
    for item in ISBN.finditer(raw):
        extracted = utila.extract_match(item)
        if verbose:
            item = utila.parse_tuple(
                item[2],
                separator='-',
                length=None,
                typ=int,
            )
            extracted: tuple = (item, extracted)
        result.append(extracted)
    return result


DOI = utila.compiles(r"""
(
    :DOI:`|
    :DOI:|
    DOI:|
    DOI
)
\s{0,3}
(
    \d{2}\s{0,2}\.\s{0,2}\d{1,4}\s{0,2}
)
\/
(
    [\d\w\/\.\-]{6,}
)
`?
""")


def doi(raw: str, verbose: bool = False) -> list:
    result = []
    for item in DOI.finditer(raw):
        extracted = utila.extract_match(item)
        if verbose:
            # TODO: VERBOSE IS NOT VERY USEFUL IN THE MORNING, REQUIRE A
            # GOOD DATA STRUCTURE
            extracted: tuple = (extracted, extracted)
        result.append(extracted)
    return result


ISSN = utila.compiles(r"""
(
    ISSN[:]?
)
\s{0,3}
(
    \d{4}-\d{4}
)
""")


def issn(raw: str, verbose: bool = False) -> list:
    """\
    >>> issn('ISSN 1095-7162', verbose=True)
    [((1095, 7162), 'ISSN 1095-7162')]
    """
    result = []
    for item in ISSN.finditer(raw):
        extracted = utila.extract_match(item)
        if verbose:
            item = utila.parse_tuple(
                item[2],
                separator='-',
                length=None,
                typ=int,
            )
            extracted: tuple = (item, extracted)
        result.append(extracted)
    return result


PATTERN = (
    isbn,
    issn,
    doi,
)


def references(raw: str, verbose: bool = False) -> list:
    """\
    >>> references(':DOI:`10.1002/9781119994398`', verbose=True)
    [((9781119994398,), '9781119994398')]
    """
    result = german.collect_and_replace(
        raw,
        pattern=PATTERN,
        verbose=verbose,
    )
    return result


VOLUME = utila.compiles(r"""
(
    (AUFLAGE|VOL\.)
    [ ]{0,2}
    (\d{1,2})
    |
    (\d)\.
    [ ]{0,2}
    (AUFLAGE)
)
""")


def volumes(text, verbose: bool = True):
    """\
    >>> volumes('(The Formation of the Classical Islamic World). Vol. 36, S. 225-234.')
    [(36, 'Vol. 36')]
    >>> volumes('Schriftsprache der Gegenwart. 5. Auflage.', verbose=False)
    [5]
    """
    result = []
    for item in VOLUME.finditer(text):
        group = item.groups()
        value = group[3] if group[3] and group[3].isnumeric() else group[2]
        if verbose:
            result.append((int(value), item[0]))
        else:
            result.append(int(value))
    return result


BIBS = utila.compiles(r"""
(
    Hrsg\.|
    Aufl\.|
    Verlag
)
""")


def bibtexts(text, verbose: bool = True):
    """\
    >>> bibtexts(' Adler und Jung. 2. Aufl. Zürich 1996.')
    [('Aufl.', 'Aufl.')]
    >>> bibtexts(' Adler und Jung. 2. Aufl. Zürich 1996.', verbose=False)
    ['Aufl.']
    """
    result = []
    for item in BIBS.finditer(text):
        if verbose:
            result.append((item[0], item[0]))
        else:
            result.append(item[0])
    return result
