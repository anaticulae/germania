# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

HEADLINES = {
    'Einleitung',
    'Anhang',
    'Anhangsverzeichnis',
    'Bibliografie',
    'Eidesstattliche Erklärung',
    'Eidesstattliche Versicherung',
    'Erklärung',
    'Internetquellen',
    'Literaturverzeichnis',
    'Quellenverzeichnis',
    'Zeitschriftenartikel',
}


def isheadline(token: str) -> bool:
    """Check if token is a headline.

    >>> isheadline('Einleitung')
    True
    >>> isheadline('    erklärung ')
    True
    """
    token = token.strip()
    token = token.title()
    if token in HEADLINES:
        return True
    return False
