# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
import typing

import knlp
import konrad
import nltk_data.lookup
import sdata
import utila

import german_data


class WordType(enum.Enum):
    MARK = enum.auto()
    PERSON = enum.auto()
    NUMBER = enum.auto()
    PRESS = enum.auto()
    YEAR = enum.auto()
    REFERENCE = enum.auto()
    UNDEFINED = enum.auto()


WordTypes = typing.List[WordType]


@utila.cacheme
def wordtype(item: str) -> WordType:  # pylint:disable=R0911
    """\
    >>> wordtype('1995').name
    'YEAR'
    """
    try:
        item = item.strip()
    except AttributeError:
        if isinstance(item, konrad.Mark):
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


@utila.cacheme
def wordtypes(item: str) -> WordTypes:
    """\
    >>> wordtypes('1996')
    {<WordType.NUMBER: 3>, <WordType.YEAR: 5>, '1996'}
    """
    try:
        item = item.lower()
    except AttributeError:
        if isinstance(item, konrad.Mark):
            return {item}
        return {WordType.UNDEFINED}
    result = {item}
    if utila.isnumber(item):
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


@utila.cacheme
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


@utila.cacheme
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


ARABIC = utila.compiles(r'(ibn|el)([ ]|\-?)\w{4,}')

PREPATTERN = utila.compiles(r'\w\.(\-|[ ])\w\.[ ]{0,3}\w{3,20}')


@utila.cacheme
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
    if sdata.isname(item):
        return True
    return False


@utila.cacheme
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
    if press in german_data.PRESS:
        return True
    if any((item for item in german_data.PRESS if item in press)):
        return True
    if sdata.rate_publisher(press):
        return True
    return False


@utila.cacheme
def iscity(city: str, length_min: int = 4) -> bool:
    """\
    >>> iscity('Berlino')
    True
    """
    city = city.strip().upper()
    if len(city) < length_min:
        return False
    if sdata.rate_city(city):
        return True
    return False


@utila.cacheme
def datums():
    # yapf:disable
    stopwords = set(knlp.STOPWORDS) - utila.splititems('der de da')
    names = (
        german_data.NAMES |
        nltk_data.lookup.NAME_MALE |
        nltk_data.lookup.NAME_FEMALE |
        nltk_data.lookup.NAME_FAMILY
    )
    noperson = (
        german_data.NOPERSON |
        german_data.PRESS |
        german_data.INSTITUTION |
        stopwords
    )
    return names, noperson
    # yapf:enable
