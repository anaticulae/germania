# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import os

import utila


class WordType(enum.Enum):
    NAME = enum.auto()
    PRESS = enum.auto()
    YEAR = enum.auto()
    UNDEFINED = enum.auto()


def wordtype(item: str) -> WordType:
    """\
    >>> wordtype('1995').name
    'YEAR'
    """
    item = item.strip()
    item = item.lower()
    if isname(item):
        return WordType.NAME
    if ispress(item):
        return WordType.PRESS
    if isyear(item):
        return WordType.YEAR
    return WordType.UNDEFINED


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


def isname(item) -> bool:
    """\
    >>> isname('Olsen')
    True
    """
    return item.lower() in NAMES


def ispress(item) -> bool:
    """\
    >>> ispress('Springer')
    True
    """
    return item.lower() in PRESS


def load_dict(path) -> set:
    assert os.path.exists(path), str(path)

    loaded = utila.file_read(path).splitlines()

    result = set(item.lower() for item in loaded)
    return result


NAMES = load_dict(os.path.join(os.path.split(__file__)[0], 'names.dict'))
PRESS = load_dict(os.path.join(os.path.split(__file__)[0], 'press.dict'))
