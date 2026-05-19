#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import pickle  # nosec

import nltk
import utila

import science_text.config


def setup(root):
    # pylint:disable=W0212
    science = nltk.load("tokenizers/punkt/{0}.pickle".format('science'))
    germania = nltk.load("tokenizers/punkt/{0}.pickle".format('germania'))
    tokenizer = nltk.load("tokenizers/punkt/{0}.pickle".format('english'))
    tokenizer._lang_vars = science_text.config.SPunktLanguageVars()
    tokenizer._params.abbrev_types |= science._params.abbrev_types
    tokenizer._params.abbrev_types |= germania._params.abbrev_types
    dumped = pickle.dumps(tokenizer)
    science_english_write(dumped, root)


def science_english_write(dumped, root):
    base = os.path.join(root, 'germania_data/ltk_data/tokenizers/punkt/')
    base = os.path.abspath(base)
    dests = [
        os.path.join(base, 'science_english.pickle'),
        os.path.join(base, 'PY3/science_english.pickle'),
    ]
    for dest in dests:
        parent = utila.path_parent(dest)
        os.makedirs(parent, exist_ok=True)
        utila.log(dest)
        utila.file_replace_binary(dest, dumped)


if __name__ == "__main__":  # pragma: no cover
    import science_text
    setup(science_text.ROOT)
