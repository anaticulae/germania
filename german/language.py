# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Language Probability
====================

This module is a very primitive approach to determine the language in
what a sentence or text is written in.

We replace this approach later with a more suiteable one. The main
approach is to set the interface and introduce complexity later.
"""

import collections
import enum

import utila

import german.word


class Language(enum.Enum):
    GERMAN = enum.auto()
    ENGLISH = enum.auto()
    FRENCH = enum.auto()
    UNKNOWN = enum.auto()


LanguageResult = collections.namedtuple(
    'LanguageResult',
    'language, probability',
)


def determine(text: str) -> LanguageResult:
    if isinstance(text, str):
        token = german.word.split_words(text, validate_sentences=False)
    else:
        token = text
    # remove signs etc.
    token = [item for item in token if isinstance(item, str)]
    ger = isgerman(token)
    eng = isenglish(token)

    ger = ger if ger >= 0.5 else 0.0
    eng = eng if eng >= 0.5 else 0.0

    ger = utila.roundme(ger)
    eng = utila.roundme(eng)

    ger = min([ger, 1.0])
    eng = min([eng, 1.0])
    print(eng)
    if ger > eng:
        return LanguageResult(language=Language.GERMAN, probability=ger)
    if eng:
        return LanguageResult(language=Language.ENGLISH, probability=ger)
    return LanguageResult(language=Language.UNKNOWN, probability=1.0)


GER = {
    'der', 'die', 'das', 'man', 'sich', 'immer', 'wieder', 'viel', 'wenig',
    'es', 'er', 'sie', 'siehe', 'bzw.'
}

ENG = {'in', 'out', 'are', 'the', 'one', 'as', 'on', 'more', 'they', 'to'}


def isgerman(token: list) -> float:
    result = 0.0
    if uppercase_ratio(token) >= 0.20:
        result += 0.5
    lower = [item.lower() for item in token]
    for item in lower:
        if item in GER:
            result += 0.05
    return result


def isenglish(token: list) -> float:
    result = 0.0
    if 0.20 <= uppercase_ratio(token) < 0.8:
        # more than 0.8 is may a title?
        result -= 0.3
    else:
        # at lot of lower case :)
        result += 0.25
    lower = [item.lower() for item in token]
    for item in lower:
        if item in ENG:
            result += 0.05
    return result


def uppercase_ratio(token):
    if not token:
        return 0.0
    upper = [item for item in token if not item.islower()]
    return len(upper) / len(token)
