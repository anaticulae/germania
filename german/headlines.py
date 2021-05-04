# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

HEADLINES = """\
Anhang
Anhangsverzeichnis
Bibliografie
Eidesstattliche Erklärung
Eidesstattliche Versicherung
Einleitung
Erklärung
Internetquellen
Literaturverzeichnis
Quellenverzeichnis
Zeitschriftenartikel
""".strip().splitlines()


def isheadline(token: str) -> bool:
    """Check if token is a headline.

    >>> isheadline('Einleitung')
    True
    >>> isheadline('    erklärung ')
    True
    >>> isheadline('Vorteile einer Steuererklärung')
    False
    """
    token = token.strip()
    if utila.similar(HEADLINES, token, maxdiff=0.85):
        return True
    return False
