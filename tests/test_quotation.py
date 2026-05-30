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
import tests.test_sentence_split


def test_quotation_extract():
    sentences = germania.sentence_tokenize(tests.test_sentence_split.STANDARD)
    expected = [
        (0, 3),
        (9, 14),
    ]
    first_quotes = germania.extract_quotes(sentences[0])
    assert first_quotes == expected
    expected = [
        (4, 7),
    ]
    second_quotes = germania.extract_quotes(sentences[1])
    assert second_quotes == expected


def test_quotation_raw():
    sentences = germania.sentence_tokenize(tests.test_sentence_split.STANDARD)
    expected = [
        (0, 3),
        (9, 14),
    ]
    splitted = germania.word_tokenize(sentences[0])
    raw = germania.raw_quotation(splitted, expected)
    assert len(raw) == 2
    expected = [
        (4, 7),
    ]
    splitted = germania.word_tokenize(sentences[1])
    raw = germania.raw_quotation(splitted, expected)
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
    extracted = germania.extract_quotes(QUOTE_IN_TEXT)
    # TODO: INVESTIGATE WHAT IS THE RIGHT ONE
    expected = [(29, 64)]
    assert extracted == expected

    splitted = germania.word_tokenize(QUOTE_IN_TEXT, validate_sentences=False)

    raw = germania.raw_quotation(splitted, extracted)
    assert len(raw) == 1


ENGLISH = """\
Kaplan/Haenlein (2009) schreiben
dazu: “In our view […] Social Media is a group of Internet-based
applications that build on the ideological and technological foundations
of Web 2.0, and that allow the creation and exchange of User Generated
Content”12.
"""


def test_parse_quote_english():
    extracted = germania.extract_quotes(ENGLISH, lang=konradus.ENGLISH)
    assert extracted == [(9, 49)]
