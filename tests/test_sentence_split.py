# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad
import pytest

import german

EXAMPLE = """\
Viele Philosophen und Psychologen ließen sich von der Beziehung zwischen \
Denken und Fühlen faszinieren. Die Annahme, dass „warme“ Emotionen und \
„kalte“ Kognitionen – umgangssprachlich „Herz und V ernunft“ – \
getrennte, gegensätzliche Systeme seien, prägte westliche Philosophen \
und Wissenschaftler über Jahrhunderte. Erst während der letzten 3 Jahre \
setzte sich langsam eine Meinung in Verhaltens- und Neurowissenschaften \
durch, welche die strikte Trennung obsolet werden ließ (Scherer, 1993). \
Nach heutiger Auffassung interagieren beide Systeme nicht nur \
miteinander, diese Interaktion ist sogar notwendig und hat sich \
phylogenetisch durchgesetzt (Ochsner & Gross, 2005). So kam es zu einem \
Boom, der die Auswirkungen von Emotionen auf kognitive Prozesse, \
angefangen bei Entscheidungsfindung bis hin zu Gedächtnis, in \
zahlreichen Studien untersuchte Phelps (2006). Die Leistung des \
Arbeitsgedächtnisses lässt sich durch eine Reihe von Aufgaben testen, \
wie z. B. die Zahlenspanne (digit span; Richardson, 2007) oder die \
Sternberg-Aufgabe (Sternberg, 1966)."""


def test_split():
    sentences = german.sentence_tokenize(EXAMPLE)
    assert len(sentences) == 6
    # splitted = german.word.split(EXAMPLE)

    first = german.word_tokenize(sentences[0])
    assert len(first) == 14 + 1, first  # 14 words plus one dot

    second = german.word_tokenize(sentences[1])
    assert len(second) == 35, second

    third = german.word_tokenize(sentences[2])
    assert len(third) == 31, third

    fourth = german.word_tokenize(sentences[3])
    assert len(fourth) == 28, fourth

    fifth = german.word_tokenize(sentences[4])
    assert len(fifth) == 33, fifth

    sixth = german.word_tokenize(sentences[5])
    assert len(sixth) == 36, sixth


def test_words_fromstr():
    splitted = german.words_fromstr(EXAMPLE)
    assert len(splitted) == 178, 'algo changed'  # Hint: Value is not correct.


MERGE_DIVISION = """\
kollektive Handlungssysteme der gesellschaftlichen \
Interessenartikulation. […] Als „Heraus- \
forderer“ machen sie Anliegen geltend, die im Prozess der politischen \
Willensbildung systema-
tisch ausgeblendet werden. Sie stehen daher in konflikthafter \
Interaktion mit etablierten Akteu- \
ren – Institutionen und Organisationen – aus dem \
politisch-administrativen System (Hervorhe-
bung im Original).
"""


def test_sentence_merge_with_textbreak():
    sentences = german.sentence_tokenize(MERGE_DIVISION)
    assert len(sentences) == 3
    assert 'Herausforderer' in sentences[1]
    assert 'systematisch' in sentences[1]
    assert 'Hervorhebung' in sentences[2]


LINE_ENDING = """\
Das Web als Service-Plattform: Verschiedene Dienste bieten die \
Möglichkeit, Arbeit über das Web zu organisieren; sie übernehmen \
Aufgaben, die ehemals Desktopanwendungen vorbehalten waren (z.B. \
Terminplanung, Dokument- bzw. Datenverwaltung etc.). Kollektive \
Intelligenz: Die Nutzer beteiligen sich und generieren gemeinsam \
Inhalte. Als Paradebeispiel gilt die Plattform Wikipedia, deren Artikel \
von Nutzern selbst verfasst bzw. verändert werden.
"""


def test_sentence_split_abrreviation_and_bracket():
    sentences = german.sentence_tokenize(LINE_ENDING)
    assert len(sentences) == 3


SHORT_SENTENCE = """\
Das Web 2.0 gilt heute als eine Plattform, die sich vor allem durch die \
direkte Beteiligung der Nutzer und daraus entstehende Netzwerkeffekte, \
wie z.B. das Nutzen kollektiven Wissens auszeichnet. Partizipation und \
Kooperation sind wichtige Charakteristika des Web 2.0 – je mehr Nutzer \
beteiligt sind, desto besser wird der Dienst. Und: Durch \
Kundenbeteiligung und computergesteuertes Datenmanagement können \
Nischenmärkte und unscheinbare Webangebote im Long Tail zu kollektiver \
Stärke heranwachsen.
"""


def test_sentence_split_short():
    sentences = german.sentence_tokenize(SHORT_SENTENCE)
    assert len(sentences) == 3


MULTIPLE_SENTENCE_IN_QUOTATION = """\
Auch der SPIEGEL beschreibt eine ähnliche Situation: Die Nutzer würden \
sich selbst entblättern, so ist in einem Leitartikel aus dem Jahr 2006 \
zu lesen. Auf der Frontseite des Heftes titelt das Blatt entsprechend: \
„Ich im Internet. Wie sich die Menschheit online entblößt.“ In dem \
Artikel heißt es:
"""


def test_sentence_split_multiple_quoted_sentence():
    sentences = german.sentence_tokenize(MULTIPLE_SENTENCE_IN_QUOTATION)
    assert len(sentences) == 3
    assert sentences[-1] == 'In dem Artikel heißt es:', sentences[-1]


SINGLE_QUOTATION_IN_TEXT = """\
This is a single " quotation “ '“ charachter in text. The parser brokes \
before cause expected .“ pattern but delivers token of length 1 cause \
the single char.
"""


def test_sentence_split_single_quotation_in_text():
    sentences = german.sentence_tokenize(SINGLE_QUOTATION_IN_TEXT)
    # dont't know the right result
    assert len(sentences) == 2


STANDARD = """„Protest“, so schreibt Sigrid Baringhorst, „ist \
kommunikatives Handeln“ (1998: 327). Will man das Phänomen ‚Protest‘ \
angemessen erfassen, so gilt es zu untersuchen, wie er kommuniziert \
wird."""

MIXED = """‚Soziale Bewegung‘ – dieser Begriff beschreibt ein Gebilde, \
das analytisch schwer zu fassen ist. Van de Donk u.a. (2004b: 3) \
beschreiben soziale Bewegungen als „fuzzy and fluid phenomena often \
without clear boundaries“, und fügen hinzu: „In sum, a social movement \
is a ‚moving target’, difficult to observe.” Dennoch soll im Folgenden \
der Versuch einer Definition vorgenommen werden."""

REQUIRE_SINGLE_INSIDE = """\
Bevor die Konzepte der Privatheit und Öffentlichkeit \
systemtheoretisch näher betrachtet werden, soll vorab kurz umrissen \
werden, was darunter verstanden wird. Rössler beschreibt etwas \
Privates folgendermaßen: „‚privat‘ nennen wir einerseits Handlungs- \
und Verhaltensweisen, zum Zweiten ein bestimmtes Wissen und drittens \
Räume“ und weiter: „als privat gilt etwas dann, wenn man selbst \
den Zugang zu diesem „etwas“ kontrollieren kann“. Privatheit \
beinhaltet also den Aspekt der Zugangskontrolle seitens des \
Individuums.
"""


def test_validate_count_of_double_quotation():
    splitted = german.sentence_tokenize(REQUIRE_SINGLE_INSIDE)
    assert len(splitted) == 3


def test_split_paragraph_with_quotation():
    splitted = german.sentence_tokenize(STANDARD)
    assert len(splitted) == 2


def test_split_paragraph_with_quotation_mixed():
    splitted = german.sentence_tokenize(MIXED)
    assert len(splitted) == 3
    last = ('Dennoch soll im Folgenden der Versuch einer '
            'Definition vorgenommen werden.')
    assert splitted[-1] == last, splitted


NUMBER_IN_TEXT = """\
Aus diesen Zielen abgeleitet, resultierte Industrie 4.0 als eines von \
zehn Zukunftsprojekten im Rahmen der Hightech-Strategie.
"""


def test_split_sentence_with_number():
    splitted = german.sentence_tokenize(NUMBER_IN_TEXT)
    assert len(splitted) == 1


VERY_LONG = """\
Im Hinblick auf die weiterführenden Kapitel dieser Arbeit erscheint \
diese Definition als zielführend, da zum einen betriebswirtschaftliche \
Aspekte berücksichtigt werden und zum anderen die technische Ausrichtung \
erkennbar ist: „Der Begriff Industrie 4.0 steht für die vierte \
industrielle Revolution, eine neue Stufe der Organisation und Steuerung \
der gesamten Wertschöpfungskette über den Lebenszyklus von Produkten. \
Dieser Zyklus orientiert sich an den zunehmend individualisierten \
Kundenwünschen und erstreckt sich von der Idee, dem Auftrag über die \
Entwicklung und Fertigung, die Auslieferung eines Produkts an den \
Endkunden bis hin zum Recycling, einschließlich der damit verbundenen \
Dienstleistungen. Basis ist die Verfügbarkeit aller relevanten \
Informationen in Echtzeit durch Vernetzung aller an der Wertschöpfung \
beteiligten Instanzen sowie die Fähigkeit, aus den Daten den zu jedem \
Zeitpunkt optimalen Wertschöpfungsfluss abzuleiten. Durch die Verbindung \
von Menschen, Objekten und Systemen entstehen dynamische, \
echtzeitoptimierte und selbst organisierende, unternehmensübergreifende \
Wertschöpfungsnetzwerke, die sich nach unterschiedlichen Kriterien wie \
bspw. Kosten, Verfügbarkeit und Ressourcenverbrauch optimieren \
lassen.“27 Ein zentrales Merkmal der dargestellten Definition ist somit \
die Optimierung der Wertschöpfungskette hin zu \
unternehmensübergreifenden Wertschöpfungsnetzwerken.
"""


def test_split_sentence_with_long_citation():
    splitted = german.sentence_tokenize(VERY_LONG)
    assert len(splitted) == 5


VALID_SENTENCE = """\
„Unter dem Begriff Digitalisierung verstehen wir die Transformation von \
Geschäftsmodellen mit Hilfe von Informations- und \
Kommunikationstechnologien zur Reduktion von Schnittstellen, zur \
funktionsübergreifenden Vernetzung und zur Erhöhung der Effektivität und \
Effizienz.“16
"""


def test_split_sentence_quotation_highnumber():
    splitted = german.sentence_tokenize(VALID_SENTENCE)
    assert len(splitted) == 1


def test_split_word_quotation_highnumber():
    splitted = german.word_tokenize(VALID_SENTENCE)
    assert splitted[0] == konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN
    assert splitted[-1] == '16'


ROMAN_NUMBERS = """\
Im Jahre 872 soll nach Schweickhadt, Ritter von Sickingen, die heutige \
Pfarrkirche erbaut worden sein, hierfür gibt es aber weder Beweise durch \
Inschriften noch durch schriftliche Quellen, 1036 wurde die Siedlung \
durch König Konrad II. zum Markt erhoben, 1136 wurde das Münzrecht \
verliehen und 1139 von Papst Innozenz II. bestätigt. Die erste \
urkundliche Erwähnung geht auf das Jahr 1094 zurück wo Neunkirchen als \
„Niuwenchirgun“, als „Neue Kirche“, bezeichnet wird (vgl. BOUS (1933), \
S. 3 ff). Hier spricht Helm?
"""


@pytest.mark.xfail(reason='roman numbers does not work properly')
def test_split_roman_numbers():
    splitted = german.sentence_tokenize(ROMAN_NUMBERS)
    assert len(splitted) == 3


TABLE = """\
In beiden Durchgängen war der SAM-Arousal-Wert nach dem neutralen \
Versuchsblock geringer als in den Furcht- respektive E kel-Blöcken (s. \
Tab. 3). Zwischensubjekteffekte (Geschlecht, Versuchsleiter, Sequenz, \
Durchgang) ergaben keine signifikanten Unterschiede, weder einzeln noch \
in Interaktionen (p>,05). \
Tab. 3: Mittelwerte und Standardabweichungen für die Arousal-Werte des \
SAM im Vergleich zwischen den drei emotionalen Qualitäten (Neutral, \
Furcht und Ekel).
"""


def test_split_table_reference():
    splitted = german.sentence_tokenize(TABLE)
    assert len(splitted) == 3


HIGHNOTE_ATEND = """\
Die so genannte Post-Privacy avanciert zu einer Idealvorstellung von \
Gesellschaft, die ohne Privatsphäre auskommt, weil man ihre schützende \
Funktion einfach nicht mehr brauche.88 Post-Privacy-Anhänger hegen die \
Utopie, dass sich Toleranz und Solidarität durchsetzen werden, wenn \
sämtliche Daten von allen offenliegen und nichts mehr verdeckt gehalten \
werden muss bzw. kann. Datenschutz im Zeitalter des Internets ist nach \
ihrer Meinung nicht erstrebenswert und ohnehin unmöglich.89 So zielt \
beispielsweise der Blogger Christian Heller in seinem Buch \
„Post-Privacy. Prima leben ohne Privatsphäre“ darauf ab, seine Leser für \
„ein Leben nach der Privatsphäre“90 zu sensibilisieren.
"""
MERGE_UNBALANCED = 'in seinem Buch „Post-Privacy. Prima leben ohne Privatsphäre“ darauf ab,'


def test_split_highnote_atend():
    splitted = german.sentence_tokenize(HIGHNOTE_ATEND)
    assert len(splitted) == 4
    assert MERGE_UNBALANCED in splitted[-1]
