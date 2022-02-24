# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad

import german
import tests

SENTENCE = """\
Verkehrsanbindung der Stadt Neunkirchen An der schon immer wichtigen \
Handelsroute von Wien über den Semmering via Graz nach Triest gelegen \
wurde die Stadt von je her von Handel und Verkehr geprägt (siehe Abb. 1).
"""

SIMPLE = """\
Abbildungen 18 und 19 zeigen die Art der Anreise in der Innenstadt nach \
Geschlechtern differenziert. Die Unterschiede erweisen sich bei den \
Anteilen des KFZ und der Fußläufigkeit als relativ hoch, öffentlicher \
Verkehr und Fahrrad sind auf einem ähnlichen Niveau.

Abb. 20 und 21 zeigen die Art der Anreise im Panoramapark nach \
Geschlechtern differenziert. Der Anteil der KFZ-Benutzer ist annähernd \
gleich, die Anteile bei Fahrrad und Fußgänger jedoch sind komplementär \
zu einander. So ist der hohe KFZ-Anteil ein Zeichen dafür, dass die \
Erreichbarkeit mit dem Auto sehr gut ist und auch große \
Gratisstellplätze vorhanden sind. Der hohe Anteil an Fahrradfahrern bei \
den Männern wiederum zeugt von der guten Anbindung an das (weiter \
wachsende) Radwegenetz, der hohe Fußgängerwert bei den Frauen kann als \
eine Folge der guten innerstädtischen Lage verstanden werden.
"""


def test_words_split():
    splitted = german.word_tokenize(SENTENCE)
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


def test_words_simple_split():
    splitted = german.sentence_tokenize(SIMPLE)
    first, second, third, fourth, fifth, sixth = splitted  # pylint:disable=W0632
    first = german.word_tokenize(first)
    second = german.word_tokenize(second)
    third = german.word_tokenize(third)
    fourth = german.word_tokenize(fourth)
    fifth = german.word_tokenize(fifth)
    sixth = german.word_tokenize(sixth)
    assert len(first) == 16
    assert len(second) == 26
    assert len(third) == 15
    assert len(fourth) == 22
    assert len(fifth) == 27
    assert len(sixth) == 39


SINGLE_NUMBER = """\
Besuchsfrequenz Neunkirchen gesamt Betrachtet man die Besuchsfrequenz \
für gesamt Neunkirchen so zeigen sich nur geringste Unterschiede im \
Prozentbereich bei den beiden Geschlechtern (siehe Abb. 5 und 6) – \
insgesamt gesehen wird Neunkirchen somit von Männern wie Frauen in \
äußerst ähnlicher Häufigkeit besucht.
"""


def test_parse_single_number():
    splitted = german.word_tokenize(SINGLE_NUMBER)
    assert '5' in splitted
    assert '6' in splitted


FOUR_DOT_ZERO = """\
„Digitalisierung und Industrie 4.0 im Mittelstand – Gestaltungsmöglich \
- keiten der digitalen Infrastruktur entlang der Wertschöpfungskette”.
"""


def test_parse_four_dot_zero():
    splitted = german.word_tokenize(FOUR_DOT_ZERO)
    assert '4.0' in splitted


FLOAT_NUMBER = 'Ich hätte gerne 134.456 kg Mett. Dazu etwas Schinken bitte.'


def test_parse_float_number():
    first = german.sentence_tokenize(FLOAT_NUMBER)[0]
    splitted = german.word_tokenize(first)
    assert '134.456' in splitted


POINT_3_DOT_2_DOT = """\
Als Erhebungsmethode wurde die persönliche Befragung vor Ort mit Hilfe \
eines standardisierten Fragebogens (siehe Punkt 3.2.: Fragebogen, Abb. 3 \
und Abb. 4) Punkt 6.4.1.3 an folgenden Wochentagen ausgewählt: Dienstag, \
Freitag, Samstag im Zeitraum von Mai bis Juli 2017.
"""


def test_parse_3dot_2dot():
    sentences = german.sentence_tokenize(POINT_3_DOT_2_DOT)
    tests.assert_length(sentences, 2)
    first_words = german.word_tokenize(sentences[0])
    assert '3.2.' in first_words
    assert '6.4.1.3' in first_words


SPLIT_NUMBERS = """\
Zusätzliche Anfor­derungen an die Betriebsstrategie ergeben sich aus den \
Abgas- und Geräuschemissionen und dem Schwingungskomfort [RNB12, S. 62ff].
"""


def test_parse_numbers_in_text():
    numbers = german.word_tokenize(SPLIT_NUMBERS)
    assert 'RNB' in numbers
    assert '62' in numbers
    assert 'ff' in numbers


ABBREV = [
    'im  Sinne  von  singulären  bzw.\n',
    'typischen  Merkmalen  eines  konkreten  Individuums,  sondern  als  „Kollektividee“.\n',
    'Personen entstehen zwangsläufig'
]


def test_merge_abbreviation_at_end():
    text = ''.join(ABBREV)
    merged = german.sentence_tokenize(text)
    assert 'singulären  bzw. typischen' in str(merged)
