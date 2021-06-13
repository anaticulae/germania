# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re
import typing

import konrad
import utila

import german

Words = typing.List[str]


def word_tokenize(
    items: str,
    validate_sentences: bool = True,
    lang: konrad.Language = None,
) -> Words:
    if validate_sentences and not german.is_sentence(items):
        # Ensure to parse complete sentences.
        return None
    items = items.replace('\n', ' ')
    items = items.replace(' z. B. ', ' z.B. ')
    result = []
    current = []
    for index, char in enumerate(items):
        if char == ' ':
            handle_whitespace(result, current)
            continue
        try:
            special = konrad.matches(char, lang=lang)
        except KeyError:
            # append normal text char or number
            current.append(char)
        else:
            handle_token(result, items, current, index, char, special)
    if current:
        if items[-1] in konrad.SIGN or not validate_sentences:
            result.append(''.join(current))
            current = []
    assert not current or validate_sentences, current
    result = unplug_numbers(result)
    result = merge_numbers(result, items)
    result = merge_reference(result, items)
    return result


def handle_whitespace(result, current):
    if len(current) == 1:
        if utila.isnumber(current[0]):
            # number and space '5 '
            result.append(current[0])
            current.clear()
    elif len(current) >= 2:
        result.append(''.join(current))
        current.clear()


def handle_token(result, items, current, index, token, special):
    # evaluate sentence sign
    if dot_pattern(current, token):
        current.append(token)
        return
    if number_bracket_pattern(current, token):
        result.append(''.join(current))
        result.append(special)
        current.clear()
        # current.append(token)
        return
    if dotable_shortcut_pattern(current, token):
        current.append(token)  # TODO: REPLACE WITH SINGLE DOT
        if index != (len(items) - 1):
            return
    if len(current) >= 2:
        result.append(''.join(current))
        current.clear()
    if len(current) == 1 and utila.isnumber(current[0]):
        # Number SpecialChar 4. 2,
        result.append(current[0])
        result.append(special)
        current.clear()
        return
    # append ), ], 3., etc.
    result.append(special)


def merge_numbers(result, source) -> list:
    """\
    >>> merge_numbers(['Ich', '134', konrad.Mark.FULLSTOP, '456', 'kg'], 'Ich 134.456 kg')
    ['Ich', '134.456', 'kg']
    """
    if len(result) <= 2:
        return result
    merged = result[:2]
    for item in result[2:]:
        if not utila.isnumber(item):
            merged.append(item)
            continue
        if merged[-1] == konrad.Mark.FULLSTOP and utila.isnumber(merged[-2]):
            together = f'{merged[-2]}.{item}'
            if together not in source:
                merged.append(item)
            else:
                merged = merged[:-2] + [together]
        else:
            merged.append(item)
    return merged


def merge_reference(result, source) -> list:
    """\
    >>> merge_reference(['Punkt', '3.2', konrad.Mark.FULLSTOP, 'Helm'], 'Punkt 3.2. Helm')
    ['Punkt', '3.2.', 'Helm']
    """
    if len(result) <= 1:
        return result
    merged = result[:1]
    for item in result[1:]:
        if item != konrad.Mark.FULLSTOP and not utila.isnumber(item):
            merged.append(item)
            continue
        if not german.isreference(merged[-1]):
            merged.append(item)
            continue
        if item == konrad.Mark.FULLSTOP:
            together = f'{merged[-1]}.'
        else:
            together = f'{merged[-1]}{item}'
        if together in source:
            merged[-1] = together
        else:
            merged.append(item)
    return merged


def unplug_numbers(result):
    """\
    >>> unplug_numbers(['Hier', 'ABC134', 'S.', '32ff'])
    ['Hier', 'ABC', '134', 'S.', '32', 'ff']
    """
    result = [
        re.split(r'(\d+)', item) if isinstance(item, str) else item
        for item in result
    ]
    result = utila.flatten(result, append=True)  # pylint:disable=unexpected-keyword-arg
    result = utila.notempty(result)  # pylint:disable=E1101
    return result


def dot_pattern(current, char) -> bool:
    """\
    >>> dot_pattern(['1'], ')')
    False
    >>> dot_pattern(['3', '.', '2'], '.')
    False
    """
    # W.D.
    if len(current) == 1:
        if current[0].isnumeric():
            # 1) # TODO: VERIFY THIS COMMENT
            return False
        if current[0] not in ')]':
            return True
    if len(current) == 3 and char == '.' and current[1] == '.':
        if utila.isnumber(current[0]) and utila.isnumber(current[2]):
            # 3.2
            return False
        return True
    return False


def number_bracket_pattern(current, char) -> bool:
    """\
    >>> number_bracket_pattern(['1', '2', '3'], ')')
    True
    """
    current = ''.join(current).lower()
    if not current.isnumeric():
        return False
    if char in '])}':
        return True
    return False


def dotable_shortcut_pattern(current, char) -> bool:
    if char != '.':
        return False
    current = ''.join(current).lower() + char
    return current in konrad.ABBREVIATION_LOWER


MARKS = (
    konrad.Mark.QUOTATION_MARK,
    konrad.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
    konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    konrad.Mark.QUOTATION_MARK_SINGLE_CLOSE,
    konrad.Mark.QUOTATION_MARK_SINGLE_OPEN,
)


def contain_quotation_marks(items) -> bool:
    """\
    >>> contain_quotation_marks(['Helm', 'Schelm', 1334, konrad.Mark.QUOTATION_MARK])
    True
    >>> contain_quotation_marks((123, 'Helm'))
    False
    """
    return any(item in MARKS for item in items)
