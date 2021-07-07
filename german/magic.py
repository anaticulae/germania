# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import functools
import os
import re
import typing

import konrad
import nltk_data.lookup
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


@functools.lru_cache(maxsize=4096)
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


@functools.lru_cache(maxsize=4096)
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


NAMES = (german_data.NAMES | nltk_data.lookup.NAME_MALE |
         nltk_data.lookup.NAME_FEMALE | nltk_data.lookup.NAME_FAMILY)
NOPERSON = german_data.NOPERSON | german_data.PRESS | german_data.INSTITUTION


def isperson(item: str) -> bool:
    """\
    >>> isperson('Olsen')
    True
    >>> isperson('Ibn Helmut')
    True
    >>> isperson('EL-Wateria')
    True
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
    """
    item = item.strip().lower()
    if item in NOPERSON:
        return False
    if item in NAMES:
        return True
    for char in '-’':
        if char not in item:
            continue
        if any(isperson(name) for name in item.split(char)):
            return True
    arabic = r'(ibn|el)([ ]|\-?)\w{4,}'
    if re.match(arabic, item, re.IGNORECASE):
        return True
    return False


def ispress(press: str) -> bool:
    """\
    >>> ispress('Springer')
    True
    >>> ispress('De Gruyter')
    True
    """
    press = press.strip().lower()
    if press in german_data.PRESS:
        return True
    if any((item for item in german_data.PRESS if item in press)):
        return True
    return False


def load_dict(path) -> set:
    assert os.path.exists(path), str(path)
    loaded = utila.file_read(path).splitlines()
    result = set(item.lower() for item in loaded)
    return result
