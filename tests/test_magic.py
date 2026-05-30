# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import utilo

import germania

NOPERSONS = utilo.splitlines("""\
Duden. Rechtschreibung
Duden
""")


@pytest.mark.parametrize(
    'raw',
    [pytest.param(item, id=item) for item in NOPERSONS],
)
def test_noperson(raw):
    assert not germania.isperson(raw)


@pytest.mark.parametrize(
    'raw',
    [pytest.param(item, id=item) for item in NOPERSONS],
)
def test_authors(raw):
    parsed = germania.authors(raw)
    decided = germania.authors_decide(parsed)
    assert isinstance(decided[0], iamraw.NoPerson)
