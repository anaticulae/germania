# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad
import utila

Sentences = utila.Strings


def split_sentences(text: str) -> Sentences:  # pylint:disable=R1260,R0912
    """Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split without any newlines
    Returns:
        list of splitted sentences
    """
    # TODO: REPLACE WITH EXTERNAL SMART ALTERNATIVE, facebook, google or
    # something else.
    # TODO: MAKE ROBUST AGAINST WHITE SPACE
    result = []
    current = []
    for token in split_token(text):
        current.append(token)
        token = token.lower()  # make approach more robust
        lastchar = token[-1]
        if lastchar == '.':
            if len(token) == 2:
                # W. G.
                continue
            if token in konrad.ABBREVIATION_LOWER:
                continue
            if token[:-1].isnumeric():
                # 1.; 13.
                continue
            if token.startswith('(') and not token.endswith(').'):
                # (z.B.), Phelps (2006).
                continue
        if lastchar in konrad.SIGN:
            if token.startswith('('):
                # (2004b: 3) SKIP
                # (2006).    NOSKIP
                if token[-2] != ')':
                    continue
            if open_quotation_mark(current):
                continue
            result.append(' '.join(current))
            current = []
        if lastchar in '’”“':  # TODO: LOOK DEEPER
            if len(token) == 1:
                # example: this is " a nice char
                # perseve index error of following sign check.
                pass
            elif token[-2] in konrad.SIGN:
                # to observe.” Dennoch
                result.append(' '.join(current))
                current = []
    if current:
        result.append(' '.join(current))
    return result


def open_quotation_mark(tokens):
    # TODO: MOVE TO KONRAD PACKAGE
    count = 0
    # TODO: CHECK DIFFERENT DOUBLE QUOTATION MARK SIGNS
    for token in tokens:
        count += token.count('„')
        count -= token.count('”')
        count -= token.count('“')
    return count > 0


QUOTATION_CLOSE_SIGNS = '"”“'  # TODO: REPLACE WITH KONRAD


def is_sentence(sentence: str, min_length: int = 4):
    if len(sentence) < min_length:  # TODO: HOLY VALUE
        # sentence is too short
        return False
    length = len(sentence)
    dotcount = sentence.count('.')
    percent_sentence = sentence.count('.') / length if length else 0.0

    if dotcount >= 3 and percent_sentence > 0.04:  # TODO: HOLY VALUE
        # sentence contains too much dots, maybe a toc line
        return False
    splitted = split_sentences(sentence)
    if len(splitted) > 1:
        return False
    token = split_token(splitted[0])
    if is_sentence_closed(token):
        return True
    return False


def is_sentence_closed(token: list) -> bool:
    """Check that the last character of the last token of a sentences contains
    a sentence close sign."""
    assert token, 'empty sentence'
    assert isinstance(token, (list, tuple)), type(token)
    last = token[-1].strip()
    last_char = last[-1]
    if last_char in konrad.SIGN:
        # ... hello?
        return True
    if len(last) < 2:
        return False
    before_last_char = last[-2]
    if last_char in QUOTATION_CLOSE_SIGNS:
        # ... hello."
        if before_last_char in konrad.SIGN:
            return True
    return False


def split_token(text: str, normalize: bool = True):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    if normalize:
        tokens = [token for token in tokens if token]
    return tokens
