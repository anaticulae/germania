# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

Sentences = typing.List[str]


def split_sentences(text: str) -> Sentences:
    """Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split without any newlines
    Returns:
        list of splitted sentences"""
    # TODO: REPLACE WITH EXTERNAL SMART ALTERNATIVE, facebook, google or
    # something else.
    result = []
    current = []
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    for token in tokens:
        if not token:
            continue
        current.append(token)
        token = token.lower()  # make approach more robust
        lastchar = token[-1]
        if lastchar == '.':
            if len(token) == 2:
                # W. G.
                continue
            if token in WHITELIST:
                continue
            if token[:-1].isnumeric():
                # 1.; 13.
                continue
            if token.startswith('(') and not token.endswith(').'):
                # (z.B.), Phelps (2006).
                continue
        if lastchar in SIGN:
            result.append(' '.join(current))
            current = []
    if current:
        result.append(' '.join(current))
    return result


def is_sentence_closed(token: list) -> bool:
    """Check that the last character of the last token of a sentences contains
    a sentence close sign."""
    assert token, 'empty sentence'
    last = token[-1].strip()
    last_char = last[-1]
    return last_char in SIGN


def is_sentence(sentence: str):
    if len(sentence) <= 5:  # TODO: HOLY VALUE
        # sentence is too short
        return False
    if sentence.count('.') >= 5:  # TODO: HOLY VALUE
        # sentence contains too much dots, maybe a toc line
        return False
    return len(split_sentences(sentence)) == 1 and (sentence[-1] in SIGN)


SIGN = {
    '!',
    '.',
    ':',
    '?',
}

# TODO: MOVE TO DUDEN PACKAGE
WHITELIST = {
    'Abb.',
    'Aufl.',
    'Bd.',
    'Co.',
    'Diss.',
    'Dok.',
    'Forts.',
    'Hrsg.',
    'Jg.',
    'S.',
    'Sp.',
    'Verf.',
    'Verl.',
    'Vol.',
    'a.a.O.',
    'al.',
    'bzw.',
    'ca.',
    'etc.',
    'f.',
    'ff.'
    'ggf.',
    'lat.',
    'mind.',
    'o.J.',
    'o.V.',
    'o.Ä',
    'usw.',
    'vgl.',
    'z.B.',
}
WHITELIST = {item.lower() for item in WHITELIST}

# a.a.O. = am angeführten Ort
# Jg. = Jahrgang
# Aufl. = Auflage
# o.J. = ohne Jahresangabe
# Bd. = Band
# o.V. = ohne Verfasserangabe
# Diss. = Dissertation
# S. = Seite
# Dok. = Dokument
# s. = siehe
# f. = (die) folgende
# Sp. = Spalte
# Verf. = Verfasser
# Forts. = Fortsetzung
# Verl. = Verlag
# H. = Heft
# Vol. = Volume (Band)
# Hrsg. = Herausgeber
