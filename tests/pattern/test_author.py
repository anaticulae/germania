# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import german


def test_comma_and():
    raw = ('PEREIRA, M.G., '
           'VOLCHAN, E., '
           'SOUZA, G. G. DE, '
           'OLIVEIRA, L., '
           'CAMPAGNOLI, R. R., '
           'PINHEIRO, W. M., '
           '& PESSOA, L. ')
    parsed = german.authors(raw)
    assert len(parsed) == 7


def test_authors_decide():
    raw = 'BOBEK H., FESL M.'
    authors = german.authors(raw)
    decided = german.authors_decide(authors)
    assert all(isinstance(item, iamraw.Person) for item in decided)
