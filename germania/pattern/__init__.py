# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import germania


def matched(content: str, pattern: list) -> bool:
    """Split `content` and check to match `pattern`. Pattern is defined
    `germania.WordType` and or `konrad.Mark`."""
    # TODO: VERY SIMPLE
    tokens = germania.word_tokenize(content, validate_sentences=False)

    pattern = list(pattern)
    for token in tokens:
        if not pattern:
            return True
        wordtype = germania.wordtype(token)
        expected = pattern[0]
        if expected == wordtype:
            # remove first item
            pattern = pattern[1:]
            continue
        if wordtype == germania.WordType.MARK and expected == token:
            # matched mark
            pattern = pattern[1:]
            continue
    if pattern:
        # some pattern was not hit
        return False
    return True
