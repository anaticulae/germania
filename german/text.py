# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german.sentence
import german.word


def words_fromstr(text: str) -> german.word.Words:
    result = []
    for sentence_ in german.sentence.sentence_tokenize(text):
        for word_ in german.word.word_tokenize(
                sentence_,
                validate_sentences=False,
        ):
            result.append(word_)
    return result
