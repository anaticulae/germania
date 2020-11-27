# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import konrad
import utila

import german

Words = typing.List[str]


def split_words(
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
    for index, token in enumerate(items):
        if token == ' ':  # nosec
            handle_whitespace(result, current)
            continue
        else:
            try:
                special = konrad.matches(token, lang=lang)
            except KeyError:
                # append normal text char or number
                current.append(token)
            else:
                handle_token(result, items, current, index, token, special)
    if current:
        if items[-1] in konrad.SIGN or not validate_sentences:
            result.append(''.join(current))
            current = []
    assert not current or validate_sentences, current
    result = merge_numbers(result, items)
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


def dot_pattern(current, token) -> bool:
    """\
    >>> dot_pattern(['1'], ')')
    False
    """
    # W.D.
    if len(current) == 1:
        if current[0].isnumeric():
            # 1)
            return False
        if current[0] not in (')', ']'):
            return True
    if len(current) == 3 and token == '.' and current[1] == '.':  # nosec
        if utila.isnumber(current[0]) and utila.isnumber(current[2]):
            # 3.2
            return False
        return True
    return False


def number_bracket_pattern(current, token) -> bool:
    """\
    >>> number_bracket_pattern(['1', '2', '3'], ')')
    True
    """
    current = ''.join(current).lower()
    if not current.isnumeric():
        return False
    if token in '])}':
        return True
    return False


def dotable_shortcut_pattern(current, token) -> bool:
    if token != '.':
        return False
    current = ''.join(current).lower() + token
    return current in konrad.ABBREVIATION_LOWER


def contain_quotation_marks(items) -> True:
    for item in items:
        if item in (
                konrad.Mark.QUOTATION_MARK,
                konrad.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
                konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN,
                konrad.Mark.QUOTATION_MARK_SINGLE_CLOSE,
                konrad.Mark.QUOTATION_MARK_SINGLE_OPEN,
        ):
            return True
    return False
