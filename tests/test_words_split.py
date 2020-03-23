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
