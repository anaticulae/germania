# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import nltk.tag.perceptron

TAGGER = nltk.tag.perceptron.PerceptronTagger(load=False)
TAGGER.train([
    [('today', 'NN'), ('is', 'VBZ'), ('good', 'JJ'), ('day', 'NN')],
    [('yes', 'NNS'), ('it', 'PRP'), ('beautiful', 'JJ')],
])


def word_tag(tokens: list) -> str:
    return TAGGER.tag(tokens)
