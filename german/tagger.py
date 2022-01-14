# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools


@functools.lru_cache(maxsize=None)
def tagger():
    # lazy loading nltk
    # TODO: MOVE TO knlp
    import nltk.tag.perceptron
    result = nltk.tag.perceptron.PerceptronTagger(load=False)
    result.train([
        [('today', 'NN'), ('is', 'VBZ'), ('good', 'JJ'), ('day', 'NN')],
        [('yes', 'NNS'), ('it', 'PRP'), ('beautiful', 'JJ')],
    ])
    return result


def word_tag(tokens: list) -> str:
    return tagger().tag(tokens)
