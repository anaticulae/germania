# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import germania


def test_comma_and():
    raw = ('PEREIRA, M.G., '
           'VOLCHAN, E., '
           'SOUZA, G. G. DE, '
           'OLIVEIRA, L., '
           'CAMPAGNOLI, R. R., '
           'PINHEIRO, W. M., '
           '& PESSOA, L. ')
    parsed = germania.authors(raw)
    assert len(parsed) == 7


def test_authors_decide():
    raw = 'BOBEK H., FESL M.'
    authors = germania.authors(raw)
    decided = germania.authors_decide(authors)
    assert all(isinstance(item, iamraw.Person) for item in decided)


AUTHORS = """\
Batra, Anil; Bilke-Hentsch, Oliver (Hg.)

""".split('\n\n')


@pytest.mark.parametrize('raw, expected', [
    pytest.param(
        AUTHORS[0],
        [('Batra', 'Anil'), ('Bilke-Hentsch', 'Oliver (Hg.)')],
        id='batra',
    ),
])
def test_author_parser(raw, expected):
    parsed = germania.authors(raw)
    assert parsed == expected


NO_AUTHORS = """\
S. 2269–2283
""".strip().splitlines()


@pytest.mark.parametrize('raw', NO_AUTHORS)
def test_no_author(raw):
    parsed = germania.authors(raw)
    authors = germania.authors_decide(parsed)
    assert all((isinstance(item, iamraw.NoPerson) for item in authors))
