# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import nltk.tokenize.punkt


class SPunktLanguageVars(nltk.tokenize.punkt.PunktLanguageVars):

    _re_word_start = r"[^\(\"\`“{\[:;&\#\*@}\)]\-,]"

    _re_non_word_chars = r"(?:[?!)\";“}\]\*:@\'\({\[])"

    re_boundary_realignment = re.compile(
        r'["\')}\]“]+?(?:\s+|(?=--)|$)',
        re.MULTILINE,
    )
