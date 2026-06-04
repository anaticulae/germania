# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Language Probability
====================

Use nltk to determine language where sentence is written in.
"""

import collections
import contextlib

import konradus
import utilo

LanguageResult = collections.namedtuple(
    'LanguageResult',
    'language, probability',
)


def determine(text: str) -> LanguageResult:
    if isinstance(text, list):
        text = konradus.remove_marks(text)
    if not isinstance(text, str):
        text = ' '.join(text)
    cat = textcat()
    detected = cat.guess_language(text)
    language = konradus.Language.GERMAN
    with contextlib.suppress(KeyError):
        language = MAPPING[detected]
    return LanguageResult(language=language, probability=1.0)


def isfre(tokens: str) -> bool:
    """\
    >>> isfre('Ich bin Helmut')
    False
    >>> isfre('Bonjour monsieur.')
    True

    verify that interface support tokens
    >>> isfre('Toujour suis Luis.'.split())
    True
    """
    return determine(tokens).language == konradus.Language.FRENCH


def iseng(tokens: str) -> bool:
    """\
    >>> iseng('Ich bin Helmut')
    False

    # >>> iseng('i like fish')
    # True
    """
    return determine(tokens).language == konradus.Language.ENGLISH


def isger(tokens: str) -> bool:
    """\
    >>> isger('Kartoffelsalat')
    True
    """
    return determine(tokens).language == konradus.Language.GERMAN


MAPPING = {
    'deu': konradus.Language.GERMAN,
    'eng': konradus.Language.ENGLISH,
    # 'es': konradus.Language.SPANISH,
    'fra': konradus.Language.FRENCH,
}


@utilo.cacheme
def textcat():
    import nltk.classify.textcat
    result = nltk.classify.textcat.TextCat()
    return result
