# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import german

NOPERSONS = """\
Duden. Rechtschreibung
Duden
""".strip().splitlines()


@pytest.mark.parametrize(
    'raw',
    [pytest.param(item, id=item) for item in NOPERSONS],
)
def test_noperson(raw):
    assert not german.isperson(raw)


@pytest.mark.parametrize(
    'raw',
    [pytest.param(item, id=item) for item in NOPERSONS],
)
def test_authors(raw):
    parsed = german.authors(raw)
    decided = german.authors_decide(parsed)
    assert isinstance(decided[0], iamraw.NoPerson)
