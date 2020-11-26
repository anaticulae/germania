# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad

import german

SENTENCE = """\
Verkehrsanbindung der Stadt Neunkirchen An der schon immer wichtigen
Handelsroute von Wien über den Semmering via Graz nach Triest gelegen
wurde die Stadt von je her von Handel und Verkehr geprägt (siehe Abb. 1).
"""


def test_words_split():
    splitted = german.split_words(SENTENCE)
    expected = [
        'Verkehr',
        'geprägt',
        konrad.Mark.BRACKET_OPEN,
        'siehe',
        'Abb.',
        '1',
        konrad.Mark.BRACKET_CLOSE,
        konrad.Mark.FULLSTOP,
    ]
    current = splitted[-8:]
    assert current == expected
