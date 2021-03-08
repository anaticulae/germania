# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Language Probability
====================

Use nltk to determine language where sentence is written in.
"""

import collections
import contextlib

import konrad
import nltk.classify.textcat

LanguageResult = collections.namedtuple(
    'LanguageResult',
    'language, probability',
)


def determine(text: str) -> LanguageResult:
    cat = nltk.classify.textcat.TextCat()
    detected = cat.guess_language(text)
    language = konrad.Language.UNKNOWN
    with contextlib.suppress(KeyError):
        language = MAPPING[detected]
    return LanguageResult(language=language, probability=1.0)


def isfre(tokens: str) -> bool:
    """\
    >>> isfre('Ich bin Helmut')
    False

    iseng('Bonjour monsieur.')
    True
    """
    return determine(tokens).language == konrad.Language.FRENCH


def iseng(tokens: str) -> bool:
    """\
    >>> iseng('Ich bin Helmut')
    False

    iseng('i like fish')
    True
    """
    return determine(tokens).language == konrad.Language.ENGLISH


def isger(tokens: str) -> bool:
    """\
    >>> isger('Kartoffelsalat')
    True
    """
    return determine(tokens).language == konrad.Language.GERMAN


MAPPING = {
    'deu': konrad.Language.GERMAN,
    'eng': konrad.Language.ENGLISH,
    # 'es': konrad.Language.SPANISH,
    'fra': konrad.Language.FRENCH,
}
