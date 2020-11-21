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

import german.sentence

Words = typing.List[str]


def split_words(  # pylint:disable=R1260,R0912
        items: str,
        validate_sentences: bool = True,
        lang: konrad.Language = None,
) -> Words:
    if validate_sentences and not german.sentence.is_sentence(items):
        # Ensure to parse complete sentences.
        return None
    items = items.replace('\n', ' ')

    items = items.replace(' z. B. ', ' z.B. ')

    result = []
    current = []
    for index, token in enumerate(items):
        if token == ' ':  # nosec
            if len(current) == 1 and not utila.isnumber(current[0]):
                continue
            elif len(current) < 2:
                continue
            result.append(''.join(current))
            current = []
            continue
        else:
            try:
                special = konrad.matches(token, lang=lang)
            except KeyError:
                # append normal text char or number
                current.append(token)
            else:
                # evaluate sentence sign
                if dot_pattern(current, token):
                    current.append(token)
                    continue
                if special == konrad.Mark.FULLSTOP:
                    if index != (len(items) - 1):
                        continue
                if len(current) >= 2:
                    result.append(''.join(current))
                    current = []
                # append ), ], 3., etc.
                result.append(special)
    if current:
        if items[-1] in konrad.SIGN or not validate_sentences:
            result.append(''.join(current))
            current = []
    assert not current or validate_sentences, current
    return result


def dot_pattern(current, token):
    # W.D.
    if len(current) == 1:
        if current[0] not in (')', ']'):
            return True
    if len(current) == 3 and token == '.' and current[1] == '.':  # nosec
        if utila.isnumber(current[0]) and utila.isnumber(current[2]):
            # 3.2
            return False
        return True
    return False


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
