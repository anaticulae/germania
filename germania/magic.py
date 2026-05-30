# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> isperson('Archibald') # nltk data
True
>>> isperson('DEUTSCHE NORM DIN') # noperson list
False
>>> isperson('Vogel-Sprott')
True
>>> isperson('S. 2269–2283')
False
>>> isperson('E. D’Andrea')
True

>>> ispress('De')
False
>>> ispress('pytest Documentation')
False
"""

import enum
import re

import analp
import konradus
import ltk_data.lookup
import sdatum
import utilo

import germania_data


class WordType(enum.Enum):
    MARK = enum.auto()
    PERSON = enum.auto()
    NUMBER = enum.auto()
    PRESS = enum.auto()
    YEAR = enum.auto()
    REFERENCE = enum.auto()
    UNDEFINED = enum.auto()


WordTypes = list[WordType]


@utilo.cacheme
def wordtype(item: str) -> WordType:  # pylint:disable=R0911
    """\
    >>> wordtype('1995').name
    'YEAR'
    """
    try:
        item = item.strip()
    except AttributeError:
        if isinstance(item, konradus.Mark):
            return WordType.MARK
        return WordType.UNDEFINED
    item = item.lower()
    if isreference(item):
        return WordType.REFERENCE
    if isperson(item):
        return WordType.PERSON
    if ispress(item):
        return WordType.PRESS
    if isyear(item):
        return WordType.YEAR
    return WordType.UNDEFINED


@utilo.cacheme
def wordtypes(item: str) -> WordTypes:
    """\
    >>> wordtypes('1996')
    {<WordType.NUMBER: 3>, <WordType.YEAR: 5>, '1996'}
    """
    try:
        item = item.lower()
    except AttributeError:
        if isinstance(item, konradus.Mark):
            return {item}
        return {WordType.UNDEFINED}
    result = {item}
    if utilo.isnumber(item):
        result.add(WordType.NUMBER)
    if isreference(item):
        result.add(WordType.REFERENCE)
    if isyear(item):
        result.add(WordType.YEAR)
    if isperson(item):
        result.add(WordType.PERSON)
    if ispress(item):
        result.add(WordType.PRESS)
    return result


REFERENCE = re.compile(r'(\d+\.?)+')


@utilo.cacheme
def isreference(item: str) -> bool:
    """\
    >>> isreference('3.2.1.')
    True
    >>> isreference('1.')
    True
    >>> isreference('5.1')
    True
    >>> isreference('1')
    False
    """
    item = str(item)
    if item.isnumeric():
        return False
    return REFERENCE.match(item) is not None


@utilo.cacheme
def isyear(item: str) -> bool:
    """\
    >>> isyear(1995)
    True
    """
    try:
        item = int(item)
    except ValueError:
        return False
    return 1900 <= item <= 2030


ARABIC = utilo.compiles(r'(ibn|el)([ ]|\-?)\w{4,}')

PREPATTERN = utilo.compiles(r'\w\.(\-|[ ])\w\.[ ]{0,3}\w{3,20}')


@utilo.cacheme
def isperson(item: str, length_min: int = 3) -> bool:  # pylint:disable=R0911
    """\
    >>> isperson('Olsen')
    True
    >>> isperson('Ibn Helmut')
    True
    >>> isperson('EL-Wateria')
    True
    >>> isperson('C.-H. Lee')
    True
    """
    item = item.strip().upper()
    if len(item) < length_min:
        return False
    names, noperson = datums()
    if item in noperson:
        return False
    if item in names:
        return True
    for char in '-’':
        if char not in item:
            continue
        if any(isperson(name) for name in item.split(char)):
            return True
    if ARABIC.match(item):
        return True
    if PREPATTERN.match(item):
        # TODO: DO NOT CRUMBLE SINGLE AND DOUBLE NAMES?
        return True
    if sdatum.isname(item):
        return True
    return False


@utilo.cacheme
def ispress(press: str, length_min: int = 6) -> bool:
    """\
    >>> ispress('Springer')
    True
    >>> ispress('De Gruyter')
    True
    """
    press = press.strip().upper()
    if len(press) < length_min:
        return False
    if press in germania_data.PRESS:
        return True
    if any((item for item in germania_data.PRESS if item in press)):
        return True
    if sdatum.rate_publisher(press):
        return True
    return False


@utilo.cacheme
def iscity(city: str, length_min: int = 4) -> bool:
    """\
    >>> iscity('Berlino')
    True
    """
    city = city.strip().upper()
    if len(city) < length_min:
        return False
    if sdatum.rate_city(city):
        return True
    return False


@utilo.cacheme
def datums():
    # yapf:disable
    stopwords = set(analp.STOPWORDS) - utilo.splititems('der de da')
    names = (
        germania_data.NAMES |
        ltk_data.lookup.NAME_MALE |
        ltk_data.lookup.NAME_FEMALE |
        ltk_data.lookup.NAME_FAMILY
    )
    noperson = (
        germania_data.NOPERSON |
        germania_data.PRESS |
        germania_data.INSTITUTION |
        stopwords
    )
    return names, noperson
    # yapf:enable
