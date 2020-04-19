# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import enum
import typing

import konrad

import german.sentence

Words = typing.List[str]


class Mark(enum.Enum):
    FULLSTOP = enum.auto()  # .
    COMMA = enum.auto()  # ,
    COLON = enum.auto()  # :
    SEMICOLON = enum.auto()  # ;
    QUESTION_MARK = enum.auto()  #?
    EXCLAMATION_MARK = enum.auto()  # !
    AND = enum.auto()  # &
    APOSTROPHE = enum.auto()  # '
    QUOTATION_MARK_DOUBLE_OPEN = enum.auto()
    QUOTATION_MARK_DOUBLE_CLOSE = enum.auto()
    QUOTATION_MARK_SINGLE_OPEN = enum.auto()
    QUOTATION_MARK_SINGLE_CLOSE = enum.auto()
    HYPHEN = enum.auto()  # - short dash
    DASH = enum.auto()  # -
    DOTS = enum.auto()  # ...
    BRACKET = enum.auto()  # ()
    BRACKET_OPEN = enum.auto()  # (
    BRACKET_CLOSE = enum.auto()  # )
    SQUARE_BRACKET = enum.auto()  # [ ]
    SQUARE_BRACKET_OPEN = enum.auto()  # [
    SQUARE_BRACKET_CLOSE = enum.auto()  #  ]
    QUOTATION_MARK = enum.auto()  # '' ""

    @classmethod
    def fromstr(cls, item: str):
        return MATCH[item]


Marks = typing.List[Mark]

MATCH = {
    '.': Mark.FULLSTOP,
    ',': Mark.COMMA,
    ':': Mark.COLON,
    ';': Mark.SEMICOLON,
    '?': Mark.QUESTION_MARK,
    '!': Mark.EXCLAMATION_MARK,
    "&": Mark.AND,
    "„": Mark.QUOTATION_MARK_DOUBLE_OPEN,
    "“": Mark.QUOTATION_MARK_DOUBLE_CLOSE,
    # "„": Mark.QUOTATION_MARK_SINGLE_OPEN,
    # "“": Mark.QUOTATION_MARK_SINGLE_CLOSE,
    "’": Mark.APOSTROPHE,
    "'": Mark.APOSTROPHE,
    '-': Mark.HYPHEN,
    '–': Mark.DASH,
    '...': Mark.DOTS,
    '()': Mark.BRACKET,
    '(': Mark.BRACKET_OPEN,
    ')': Mark.BRACKET_CLOSE,
    '[': Mark.SQUARE_BRACKET_OPEN,
    ']': Mark.SQUARE_BRACKET_CLOSE,
    # '""': Mark.QUESTION_MARK,
}


def split_words(items: str, validate_sentences: bool = True):  # pylint:disable=R1260,R0912
    if validate_sentences and not german.sentence.is_sentence(items):
        # Ensure to parse complete sentences.
        return None
    items = items.replace('\n', ' ')

    items = items.replace(' z. B. ', ' z.B. ')

    result = []
    current = []
    for index, token in enumerate(items):
        if token == ' ':
            if len(current) == 1 and not isnumber(current[0]):
                continue
            elif len(current) < 2:
                continue
            result.append(''.join(current))
            current = []
            continue
        else:
            try:
                special = MATCH[token]
            except KeyError:
                # append normal text char or number
                current.append(token)
            else:
                # evaluate sentence sign
                if dot_pattern(current, token):
                    current.append(token)
                    continue
                if special == Mark.FULLSTOP:
                    if index != (len(items) - 1):
                        continue
                if len(current) >= 2:
                    result.append(''.join(current))
                    current = []
                # append ), ], 3., etc.
                result.append(special)
    if current and items[-1] in konrad.SIGN:
        result.append(''.join(current))
        current = []
    if validate_sentences:
        assert not current, current
    return result


def dot_pattern(current, token):
    # W.D.
    if len(current) == 1:
        if current[0] not in (')', ']'):
            return True
    if len(current) == 3 and token == '.' and current[1] == '.':
        if isnumber(current[0]) and isnumber(current[2]):
            # 3.2
            return False
        return True
    return False


def isnumber(item):
    with contextlib.suppress(ValueError):
        _ = int(item)
        return True
    return False
