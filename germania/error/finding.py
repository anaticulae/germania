# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import enum

import iamraw


class TextErrorType(enum.Enum):
    MISSING = enum.auto()
    """Text token is missing"""
    STYLE = enum.auto()
    """Violation against good style"""
    RULE = enum.auto()
    """Writing is against the writing laws"""
    DUPLICATED = enum.auto()
    """Copy paste error"""
    REPLACEMENT = enum.auto()
    """Replace this content"""
    UNDEFINED = enum.auto()
    """No special state"""


@dataclasses.dataclass
class TextError:
    title: str = None
    text: str = None
    state: TextErrorType = None
    location: iamraw.Location = None
    raw: str = None
    better: str = None
    debug_method: str = None
    """Name of method which had determined this error."""


TextErrors = list[TextError]
