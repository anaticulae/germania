# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import tests.test_sentence_split


def test_quotation_extract():
    first, second = german.split_sentences(tests.test_sentence_split.STANDARD)  # pylint:disable=W0632
    expected = [
        (0, 3),
        (9, 14),
    ]
    first_quotes = german.extract_quotes(first)
    assert first_quotes == expected

    expected = [
        (4, 7),
    ]
    second_quotes = german.extract_quotes(second)
    assert second_quotes == expected


def test_quotation_raw():
    first, second = german.split_sentences(tests.test_sentence_split.STANDARD)  # pylint:disable=W0632
    expected = [
        (0, 3),
        (9, 14),
    ]
    splitted = german.split_words(first)
    raw = german.raw_quotation(splitted, expected)
    assert len(raw) == 2

    expected = [
        (4, 7),
    ]
    splitted = german.split_words(second)
    raw = german.raw_quotation(splitted, expected)
    assert len(raw) == 1


QUOTE_IN_TEXT = """\
Auf Basis der beschriebenen Treiber für die Digitalisierung und im
Hinblick auf die weiterführenden Kapitel erscheint jedoch folgende
Definition nach BECKER ET Al. als zielführend für diese Bachelorarbeit:
„Unter dem Begriff Digitalisierung verstehen wir die Transformation von
Geschäftsmodellen mit Hilfe von Informations- und
Kommunikationstechnologien zur Reduktion von Schnittstellen, zur
funktionsübergreifenden Vernetzung und zur Erhöhung der Effektivität und
Effizienz.“16 Die dargestellte Definition verdeutlicht, dass sich im
Zuge der Digitalisierung die Geschäftsmodelle der mittelständischen
Unternehmen verändern werden. Durch die funktionsübergreifende
Vernetzung im Sinne von Industrie 4.0 sind alle Unternehmensbereiche
davon betroffen.
"""


def test_parse_long_quote():
    extracted = german.extract_quotes(QUOTE_IN_TEXT)
    expected = [(29, 63)]
    assert extracted == expected

    splitted = german.split_words(QUOTE_IN_TEXT, validate_sentences=False)

    raw = german.raw_quotation(splitted, extracted)
    assert len(raw) == 1
