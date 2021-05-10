# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import knlp
import konrad
import utila

Sentences = utila.Strings


def sentence_tokenize(
        text: str,
        *,
        merge_divis: bool = True,
        normalize_newline: bool = True,
        normalize_spaces: bool = False,
) -> Sentences:  # pylint:disable=R1260,R0912
    r"""Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split containing no newlines
        merge_divis(bool): merge lines with divis together
        normalize_newline(bool): replace newline with space single space
        normalize_spaces(bool): replace multiple spaces with single one
    Returns:
        list of splitted sentences

    # >>> sentence_tokenize('Dies ist der 1. Satz. Dies ist ein zweiter Satz!')
    ['Dies ist der 1. Satz.', 'Dies ist ein zweiter Satz!']
    >>> sentence_tokenize('Dieser Satz ent-\nhält eine Trennung.', merge_divis=True)
    ['Dieser Satz enthält eine Trennung.']
    >>> sentence_tokenize('Das  sind   eindeutig zu   viele Trennungen.', normalize_spaces=True)
    ['Das sind eindeutig zu viele Trennungen.']
    >>> sentence_tokenize('Der Stadtteil Berlin-\nNeuköln liegt im Süden von Berlin.')
    ['Der Stadtteil Berlin-Neuköln liegt im Süden von Berlin.']
    """
    text = utila.normalize_text(
        text,
        merge_divis=merge_divis,
        normalize_newline=normalize_newline,
        normalize_spaces=normalize_spaces,
    )
    # tokenize sentence
    tokenized = knlp.sent_tokenize(text, language='science')
    return tokenized


def isunbalanced(sentence: str) -> bool:
    """\
    >>> isunbalanced('I am ( unbalanced')
    True
    >>> isunbalanced('I am not ( unbalanced )')
    False
    """
    pair = (('(', ')'), ('[', ']'))
    for start, close in pair:
        if sentence.count(start) != sentence.count(close):
            return True
    return False


def open_quotation_mark(tokens: list) -> int:
    # TODO: MOVE TO KONRAD PACKAGE
    count = 0
    # TODO: CHECK DIFFERENT DOUBLE QUOTATION MARK SIGNS
    for token in tokens:
        count += token.count('„')
        count -= token.count('”')
        count -= token.count('“')
    return count > 0


QUOTATION_CLOSE_SIGNS = '"”“'  # TODO: REPLACE WITH KONRAD


def is_sentence(sentence: str, min_length: int = 4) -> bool:
    if len(sentence) < min_length:  # TODO: HOLY VALUE
        # sentence is too short
        return False
    length = len(sentence)
    dotcount = sentence.count('.')
    percent_sentence = sentence.count('.') / length if length else 0.0
    if dotcount >= 3 and percent_sentence > 0.04:  # TODO: HOLY VALUE
        # sentence contains too much dots, maybe a toc line
        return False
    splitted = sentence_tokenize(sentence)
    if len(splitted) > 1:
        return False
    token = split_token(splitted[0])
    if is_sentence_closed(token):
        return True
    return False


CLOSE_SIGNS = '.?!'


def is_sentence_closed(token: list) -> bool:  # pylint:disable=R0911
    """Check that the last character of the last token of a sentences contains
    a sentence close sign.

    >>> is_sentence_closed(['Effektivität', 'und', 'Effizienz.', '“'])
    True
    """
    assert token, 'empty sentence'
    assert isinstance(token, (list, tuple)), type(token)
    last = token[-1].strip()
    last_char = last[-1]
    if last_char in konrad.SIGN:
        # ... hello?
        return True
    if len(last) == 1:
        # 'Effizienz.', '“'
        if last not in QUOTATION_CLOSE_SIGNS:
            # TODO: CHECK ALL QUOTATION SIGNS?
            return False
    else:
        before_last_char = last[-2]
        if last_char in QUOTATION_CLOSE_SIGNS:
            # ... hello."
            if before_last_char in konrad.SIGN:
                return True
    if len(token) > 3:
        before_last = token[-2]
        third_last = token[-3]
        # HACK AND INCOMPLETE
        # greater than three cause a sentence needs some words
        # DOTTED, QUOTED
        # 'Effizienz.', '“'
        # TODO: SIMPLIFY THIS, USE PERMUTATION AND TOKEN CLASSES
        if last in QUOTATION_CLOSE_SIGNS and before_last[-1] in CLOSE_SIGNS:
            return True
        if before_last in QUOTATION_CLOSE_SIGNS and last[-1] in CLOSE_SIGNS:
            return True
        if last.isnumeric() and before_last in QUOTATION_CLOSE_SIGNS and third_last[-1] in CLOSE_SIGNS: # yapf:disable
            return True
        # DOTTED, QUOTED, NUMBER
        # 'Effizienz.', '“', '16'
    return False


def split_token(text: str, normalize: bool = True):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    if normalize:
        tokens = [token for token in tokens if token]
    tokens = [split_special_chars(item) for item in tokens]
    tokens = utila.flatten(tokens)
    return tokens


SPECIAL = ['„', '“', '‘', '‚']


def split_special_chars(token):
    """\
    >>> split_special_chars('„‚privat‘')
    ['„', '‚', 'privat', '‘']
    """
    for special in SPECIAL:
        splitted = token.split(special)
        token = f' {special} '.join(splitted)
    splitted = token.split()
    return splitted
