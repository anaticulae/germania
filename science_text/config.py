# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import nltk.tokenize.punkt


class SPunktLanguageVars(nltk.tokenize.punkt.PunktLanguageVars):
    """Modifkation:
        - Quotation signs and merge them to sentence before
        - Merge citation number to sentence before: 'lassen.“27 Jetzt geht es'
    """

    _re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[”“„])"

    # \d to align citing numbers for example: lassen.“27 Jetzt geht es
    # highnote magic pattern: {{hn:143:nh}}
    re_boundary_realignment = re.compile(
        r"""
        (
            ["\')}\]“”\d]|
            (
                [ ]{0,3}                    # allow some white space before
                \{\{hn\:\d{1,4}\:nh\}\}     # highnote magic pattern
            )
        )+?
        (?:\s+|(?=--)|$)
        """,
        flags=re.MULTILINE | re.X,
    )
    sent_end_chars = '.?!:'
    internal_punctuation = ',;'
