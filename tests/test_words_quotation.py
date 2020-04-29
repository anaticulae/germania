# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german

STANDARD = """„Protest“, so schreibt Sigrid Baringhorst, „ist
kommunikatives Handeln“ (1998: 327). Will man das Phänomen ‚Protest‘
angemessen erfassen, so gilt es zu untersuchen, wie er kommuniziert
wird."""

MIXED = """‚Soziale Bewegung‘ – dieser Begriff beschreibt ein Gebilde,
das analytisch schwer zu fassen ist. Van de Donk u.a. (2004b: 3)
beschreiben soziale Bewegungen als „fuzzy and fluid phenomena often
without clear boundaries“, und fügen hinzu: „In sum, a social movement
is a ‚moving target’, difficult to observe.” Dennoch soll im Folgenden
der Versuch einer Definition vorgenommen werden."""

REQUIRE_SINGLE_INSIDE = """\
Bevor die Konzepte der Privatheit und Öffentlichkeit
systemtheoretisch näher betrachtet werden, soll vorab kurz umrissen
werden, was darunter verstanden wird. Rössler beschreibt etwas
Privates folgendermaßen: „‚privat‘ nennen wir einerseits Handlungs-
und Verhaltensweisen, zum Zweiten ein bestimmtes Wissen und drittens
Räume“ und weiter: „als privat gilt etwas dann, wenn man selbst
den Zugang zu diesem „etwas“ kontrollieren kann“. Privatheit
beinhaltet also den Aspekt der Zugangskontrolle seitens des
Individuums.
"""


def test_validate_count_of_double_quotation():
    splitted = german.split_sentences(REQUIRE_SINGLE_INSIDE)
    assert len(splitted) == 5


def test_split_paragraph_with_quotation():
    splitted = german.split_sentences(STANDARD)
    assert len(splitted) == 2


def test_split_paragraph_with_quotation_mixed():
    splitted = german.split_sentences(MIXED)
    assert len(splitted) == 4
    last = ('Dennoch soll im Folgenden der Versuch einer '
            'Definition vorgenommen werden.')
    assert splitted[-1] == last, splitted
