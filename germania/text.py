# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import germania.sentence
import germania.word


def words_fromstr(text: str) -> germania.word.Words:
    result = []
    for sentence_ in germania.sentence.sentence_tokenize(text):
        for word_ in germania.word.word_tokenize(
                sentence_,
                validate_sentences=False,
        ):
            result.append(word_)
    return result
