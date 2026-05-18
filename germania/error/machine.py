# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import utila

import germania.error.finding


class TextErrorMachine:
    """\
    >>> empty = TextErrorMachine()
    >>> empty.determine('')
    []
    """

    def determine(
        self,
        text: str,
        page: int = None,
    ) -> germania.error.finding.TextErrors:
        result = []
        todo = utila.methods(self, starts='check_')
        for method in todo:
            detected = method(text)
            if not detected:
                continue
            if not utila.iterable(detected):
                result.append(detected)
                detected.debug_method = method.__name__
                continue
            for item in detected:
                item.debug_method = method.__name__
            result.extend(detected)
        if page is not None:
            for item in result:
                with contextlib.suppress(AttributeError):
                    item.location.page = page
        return result

    def location(self, match) -> iamraw.RangedLocation:  # pylint:disable=R0201
        if not match:
            return None
        location = iamraw.RangedLocation(
            char=match.span()[0],
            char_end=match.span()[1],
        )
        return location


class PhysicMachine(TextErrorMachine):
    """\
    >>> machine = PhysicMachine()
    >>> machine.determine('The weight is 200kg. Thats a lot.', page=10)
    [TextError(...state=<TextErrorType.RULE...>, location=RangedLocation(page=10, char=13, char_end=19), raw='200kg', better='200 kg', debug_method='check_physical_spaces')]
    """

    MISSING_SPACE_BEFORE_UNIT = utila.compiles(r"""
        \W
        (
            (?P<value>\d+((\.|\,)\d+){0,1})
            (?P<unit>%|‰|kg|km/h|mmHg|mm|ms|mg/km|m|cm|V|W|Hz|mW)
        )
    """)

    def check_physical_spaces(self, text: str) -> list:
        result = []
        for match in self.MISSING_SPACE_BEFORE_UNIT.finditer(text):
            error = germania.error.finding.TextError(
                state=germania.error.finding.TextErrorType.RULE,
                better=match['value'] + ' ' + match['unit'],
                location=self.location(match),
                raw=match[1],
            )
            result.append(error)
        return result
