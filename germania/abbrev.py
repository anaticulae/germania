# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sdatum
import utilo

import germania


def find_abbrev(abbrev: str, words: list) -> str:
    """\
    >>> find_abbrev('MNU', 'Steuergebiete zugunsten multinationaler Unternehmen'.split())
    'multinationaler Unternehmen'
    >>> import germania
    >>> find_abbrev('MNU', germania.words_fromstr('Steuergebiete zugunsten multinationaler Unternehmens(MNU) ende'))
    'multinationaler Unternehmens'
    """
    lookup = sdatum.abbrev(abbrev)
    if lookup is None:
        return None
    lookup = [germania.word_normalize(item) for item in lookup]
    normalized = [
        germania.word_normalize(item) if isinstance(item, str) else item
        for item in words
    ]
    detected = germania.searches(
        patterns=lookup,
        sentence=normalized,
        tokens_complex=False,
    )
    if not detected:
        return None
    result = ' '.join(words[index] for index in utilo.rlist(*detected[0]))
    return result
