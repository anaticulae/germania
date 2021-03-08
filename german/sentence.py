# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad
import utila

Sentences = utila.Strings

SHORTCUTS = konrad.ABBREVIATION_LOWER


def sentence_tokenize(text: str) -> Sentences:  # pylint:disable=R1260,R0912
    """Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split containing no newlines
    Returns:
        list of splitted sentences

    >>> sentence_tokenize('Dies ist der 1. Satz. Dies ist ein zweiter Satz!')
    ['Dies ist der 1. Satz.', 'Dies ist ein zweiter Satz!']
    """
    # TODO: REPLACE WITH EXTERNAL SMART ALTERNATIVE, facebook, google or
    # something else.
    # TODO: MAKE ROBUST AGAINST WHITE SPACE
    result = []
    current = []
    for word in split_token(text):
        current.append(word)
        word = word.lower()  # make approach more robust
        lastchar = word[-1]
        if (word == '“' or word.isnumeric()):
            if len(current) == 1 and result:
                # merge close quotation and or number to sentence before
                result[-1] = result[-1] + word
                current.clear()
                continue
        if lastchar == '.':
            if len(word) == 2:
                # W. G.
                continue
            if word in SHORTCUTS:
                continue
            if utila.isroman(word[:-1]):
                continue
            if word[:-1].isnumeric():
                # 1.; 13.
                continue
            if word.startswith('(') and not word.endswith(').'):
                # (z.B.), Phelps (2006).
                continue
        if lastchar in konrad.SIGN:
            if word.startswith('('):
                # (2004b: 3) SKIP
                # (2006).    NOSKIP
                if word[-2] != ')':
                    continue
            # if open_quotation_mark(current):
            # TODO: ENABLE LATER?
            #     continue
            result.append(' '.join(current))
            current = []
        if lastchar in '’”“':  # TODO: LOOK DEEPER
            if len(word) == 1:
                # example: this is " a nice char
                # perseve index error of following sign check.
                pass
            elif word[-2] in konrad.SIGN:
                # to observe.” Dennoch
                result.append(' '.join(current))
                current = []
    if current:
        result.append(' '.join(current))
    result = merge_unbalanced(result)
    return result


def merge_unbalanced(sentences: list) -> list:
    if not sentences:
        return sentences
    result = [sentences[0]]
    for before, sentence in enumerate(sentences[1:]):
        if not isunbalanced(sentence):
            result.append(sentence)
            continue
        if isunbalanced(sentences[before]):
            result.append(result.pop() + ' ' + sentence)
        else:
            result.append(sentence)
    return result


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
