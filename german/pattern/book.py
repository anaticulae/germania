# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Examples:
=========

ISBN
----

>>> isbn('ISBN 978-0-9745607-3-1.')
['ISBN 978-0-9745607-3-1']
>>> isbn('ISBN 13: 978-1292-02572-8')
['ISBN 13: 978-1292-02572-8']
>>> isbn('ISBN 978-0-9745607-3-1.')
['ISBN 978-0-9745607-3-1']
>>> isbn('ISBN 0-201-56317-7')
['ISBN 0-201-56317-7']
>>> isbn('ISBN 0-471-22361-1.')
['ISBN 0-471-22361-1']
>>> isbn('ISBN 13: 9781119994398')
['ISBN 13: 9781119994398']
>>> isbn('ISBN 3540429883.')
['ISBN 3540429883']
>>> isbn('ISBN: 0521540518')
['ISBN: 0521540518']
>>> isbn('isbn: 978-1-931971-16-4.')
['isbn: 978-1-931971-16-4']
>>> isbn('isbn:1-931666-22-9')
['isbn:1-931666-22-9']
>>> isbn('isbn:978-1-4503-2758-9.')
['isbn:978-1-4503-2758-9']

ISSN
----

>>> issn('ISSN 1095-7162')
['ISSN 1095-7162']

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
>>> doi('doi: 10.1145/2723372.2742797.url')
['doi: 10.1145/2723372.2742797.url']
"""

import utila

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


def isbn(raw: str) -> list:
    result = []
    for item in ISBN.finditer(raw):
        extracted = utila.extract_match(item)
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
    \d{2}\.\d{1,4}
)
\/
(
    [\d\w\/\.\-]{6,}
)
`?
""")


def doi(raw: str) -> list:
    result = []
    for item in DOI.finditer(raw):
        extracted = utila.extract_match(item)
        result.append(extracted)
    return result


ISSN = utila.compiles(r"""
(
    ISSN
)
\s{0,3}
(
    \d{4}-\d{4}
)
""")


def issn(raw: str) -> list:
    result = []
    for item in ISSN.finditer(raw):
        extracted = utila.extract_match(item)
        result.append(extracted)
    return result
