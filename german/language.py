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

import konrad
import utila

import german.word

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
    fra = isfrench(token)

    ger = ger if ger >= 0.5 else 0.0
    eng = eng if eng >= 0.5 else 0.0
    fra = fra if fra >= 0.75 else 0.0

    # TODO: IMPROVE AFTER UPGRADING UTILA
    ger = utila.roundme(ger)
    eng = utila.roundme(eng)
    fra = utila.roundme(fra)

    ger = min([ger, 1.0])
    eng = min([eng, 1.0])
    fra = min([fra, 1.0])

    if fra:
        return LanguageResult(language=konrad.Language.FRENCH, probability=fra)
    if ger > eng:
        return LanguageResult(language=konrad.Language.GERMAN, probability=ger)
    if eng:
        return LanguageResult(language=konrad.Language.ENGLISH, probability=eng)
    return LanguageResult(language=konrad.Language.UNKNOWN, probability=1.0)


GER = {
    'der', 'die', 'das', 'man', 'sich', 'immer', 'wieder', 'viel', 'wenig',
    'es', 'er', 'sie', 'siehe', 'bzw.'
}

ENG = {'in', 'out', 'are', 'the', 'one', 'as', 'on', 'more', 'they', 'to'}

FRA = {'au', 'de', 'des', 'en', 'en', 'la', 'le', 'les'}


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


def isfrench(token: list) -> float:
    result = 0.0
    lower = [item.lower() for item in token]
    if accent_ration(lower) >= 0.1:
        result = result + 0.35
    for item in lower:
        if item in FRA:
            result += 0.05
    return result


def uppercase_ratio(token):
    if not token:
        return 0.0
    upper = [item for item in token if not item.islower()]
    return len(upper) / len(token)


def accent_ration(token):
    if not token:
        return 0.0
    accents = [item for item in token if 'é' in item]
    return len(accents) / len(token)
