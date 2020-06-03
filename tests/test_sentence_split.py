# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german.sentence
import german.word

EXAMPLE = """\
Viele Philosophen und Psychologen ließen sich von der Beziehung zwischen
Denken und Fühlen faszinieren. Die Annahme, dass „warme“ Emotionen und
„kalte“ Kognitionen – umgangssprachlich „Herz und V ernunft“ –
getrennte, gegensätzliche Systeme seien, prägte westliche Philosophen
und Wissenschaftler über Jahrhunderte. Erst während der letzten 3 Jahre
setzte sich langsam eine Meinung in Verhaltens- und Neurowissenschaften
durch, welche die strikte Trennung obsolet werden ließ (Scherer, 1993).
Nach heutiger Auffassung interagieren beide Systeme nicht nur
miteinander, diese Interaktion ist sogar notwendig und hat sich
phylogenetisch durchgesetzt (Ochsner & Gross, 2005). So kam es zu einem
Boom, der die Auswirkungen von Emotionen auf kognitive Prozesse,
angefangen bei Entscheidungsfindung bis hin zu Gedächtnis, in
zahlreichen Studien untersuchte Phelps (2006). Die Leistung des
Arbeitsgedächtnisses lässt sich durch eine Reihe von Aufgaben testen,
wie z. B. die Zahlenspanne (digit span; Richardson, 2007) oder die
Sternberg-Aufgabe (Sternberg, 1966)."""


def test_split():
    sentences = german.sentence.split_sentences(EXAMPLE)
    assert len(sentences) == 6
    # splitted = german.word.split(EXAMPLE)

    first = german.word.split_words(sentences[0])
    assert len(first) == 14 + 1, first  # 14 words plus one dot

    second = german.word.split_words(sentences[1])
    assert len(second) == 35, second

    third = german.word.split_words(sentences[2])
    assert len(third) == 30, third

    fourth = german.word.split_words(sentences[3])
    assert len(fourth) == 28, fourth

    fifth = german.word.split_words(sentences[4])
    assert len(fifth) == 33, fifth

    sixth = german.word.split_words(sentences[5])
    assert len(sixth) == 36, sixth


def test_words_fromstr():
    splitted = german.words_fromstr(EXAMPLE)
    assert len(splitted) == 177, 'algo changed'  # Hint: Value is not correct.


MERGE_DIVISION = """\
kollektive Handlungssysteme der gesellschaftlichen
Interessenartikulation. […] Als „Heraus-
forderer“ machen sie Anliegen geltend, die im Prozess der politischen
Willensbildung systema-
tisch ausgeblendet werden. Sie stehen daher in konflikthafter
Interaktion mit etablierten Akteu-
ren – Institutionen und Organisationen – aus dem
politisch-administrativen System (Hervorhe-
bung im Original).
"""


def test_sentence_merge_with_textbreak():
    sentences = german.split_sentences(MERGE_DIVISION)
    assert len(sentences) == 3
    assert 'Herausforderer' in sentences[1]
    assert 'systematisch' in sentences[1]
    assert 'Hervorhebung' in sentences[2]


LINE_ENDING = """\
Das Web als Service-Plattform: Verschiedene Dienste bieten die
Möglichkeit, Arbeit über das Web zu organisieren; sie übernehmen
Aufgaben, die ehemals Desktopanwendungen vorbehalten waren (z.B.
Terminplanung, Dokument- bzw. Datenverwaltung etc.). Kollektive
Intelligenz: Die Nutzer beteiligen sich und generieren gemeinsam
Inhalte. Als Paradebeispiel gilt die Plattform Wikipedia, deren Artikel
von Nutzern selbst verfasst bzw. verändert werden.
"""


def test_sentence_split_abrreviation_and_bracket():
    sentences = german.split_sentences(LINE_ENDING)
    assert len(sentences) == 5


SHORT_SENTENCE = """\
Das Web 2.0 gilt heute als eine Plattform, die sich vor allem durch die
direkte Beteiligung der Nutzer und daraus entstehende Netzwerkeffekte,
wie z.B. das Nutzen kollektiven Wissens auszeichnet. Partizipation und
Kooperation sind wichtige Charakteristika des Web 2.0 – je mehr Nutzer
beteiligt sind, desto besser wird der Dienst. Und: Durch
Kundenbeteiligung und computergesteuertes Datenmanagement können
Nischenmärkte und unscheinbare Webangebote im Long Tail zu kollektiver
Stärke heranwachsen.
"""


def test_sentence_split_short():
    sentences = german.split_sentences(SHORT_SENTENCE)
    assert len(sentences) == 4


MULTIPLE_SENTENCE_IN_QUOTATION = """\
Auch der SPIEGEL beschreibt eine ähnliche Situation: Die Nutzer würden
sich selbst entblättern, so ist in einem Leitartikel aus dem Jahr 2006
zu lesen. Auf der Frontseite des Heftes titelt das Blatt entsprechend:
„Ich im Internet. Wie sich die Menschheit online entblößt.“ In dem
Artikel heißt es:
"""


def test_sentence_split_multiple_quoted_sentence():
    sentences = german.split_sentences(MULTIPLE_SENTENCE_IN_QUOTATION)
    assert len(sentences) == 5
    assert sentences[-1] == 'In dem Artikel heißt es:', sentences[-1]


SINGLE_QUOTATION_IN_TEXT = """\
This is a single " quotation “ '“ charachter in text. The parser brokes
before cause expected .“ pattern but delivers token of length 1 cause
the single char.
"""


def test_sentence_split_single_quotation_in_text():
    sentences = german.split_sentences(SINGLE_QUOTATION_IN_TEXT)
    assert len(sentences) == 3


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
