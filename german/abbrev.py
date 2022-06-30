# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sdata
import utila

import german


def find_abbrev(abbrev: str, words: list) -> str:
    """\
    >>> find_abbrev('MNU', 'Steuergebiete zugunsten multinationaler Unternehmen'.split())
    'multinationaler Unternehmen'
    >>> import german
    >>> find_abbrev('MNU', german.words_fromstr('Steuergebiete zugunsten multinationaler Unternehmens(MNU) ende'))
    'multinationaler Unternehmens'
    """
    lookup = sdata.abbrev(abbrev)
    if lookup is None:
        return None
    lookup = [german.word_normalize(item) for item in lookup]
    normalized = [
        german.word_normalize(item) if isinstance(item, str) else item
        for item in words
    ]
    detected = german.searches(patterns=lookup, sentence=normalized)
    if not detected:
        return None
    result = ' '.join(words[index] for index in utila.rlist(*detected[0]))
    return result
