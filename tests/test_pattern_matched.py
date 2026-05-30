# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konradus

import germania

EXAMPLE = """\
JUERGEN LEOHOLD: Communication Requirements for Automotive Systems. In:
WFCS 2004 5thIEEE Workshop on Factory Communication Systems (2004)

AGARWAL, B.B. ; TAYAL, S.P.: Software Engineering and Testing. Jones &
Bartlett Learning, 2009 (Jones and Bartlett series in computer science)

""".split('\n\n')

NOT_MATCHED = """\
Norm DIN 55350-11 2008. Begriffe zum Qualitätsmanagement

Norm ISO 11898 2003. Road vehicles - Controller area network(CAN)

""".split('\n\n')

EXPECTED = [
    germania.WordType.PERSON, konradus.Mark.COLON, germania.WordType.YEAR
]


def test_pattern_matched():
    matched = germania.matched(EXAMPLE[0], EXPECTED)
    assert matched

    matched = germania.matched(EXAMPLE[1], EXPECTED)
    assert matched


def test_pattern_not_matched():
    matched = germania.matched(NOT_MATCHED[0], EXPECTED)
    assert not matched
