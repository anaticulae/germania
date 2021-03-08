#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import pickle
import re
import sys

import hugedata
import nltk.tokenize.punkt
import utila

import german_data
import science_text.config


def train(src: str, dest: str, verbose: bool = False):
    utila.log(f'load corpus: {src}')

    if isinstance(src, list):
        content = [utila.file_read(item) for item in src]
        text = utila.NEWLINE.join(content)
    else:
        text = utila.file_read(src)
    # Make a new Tokenizer
    lang_vars = science_text.config.SPunktLanguageVars()
    trainer = nltk.tokenize.punkt.PunktTrainer(lang_vars=lang_vars)
    trainer.train(text, verbose=verbose)

    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(
        train_text=trainer.get_params(),
        lang_vars=lang_vars,
    )

    utila.log(f'dump tokenizer: {dest}')
    dumped = pickle.dumps(tokenizer)
    utila.file_replace_binary(dest, dumped)


SOURCES = [
    hugedata.LIT_MASTER072,
    hugedata.LIT_MASTER075,
    hugedata.LIT_MASTER083,
    hugedata.LIT_MASTER089,
    hugedata.UTILS_ABBREVIATION,
]

if __name__ == "__main__":
    verbose = 'verbose' in sys.argv

    tmp = utila.tmpfile(german_data.ROOT)
    train(SOURCES, tmp, verbose=verbose)

    dumped = utila.file_read_binary(tmp)
    root = os.path.join(german_data.ROOT, 'german_data')
    dests = [
        os.path.join(root, 'nltk_data/tokenizers/punkt/science.pickle'),
        os.path.join(root, 'nltk_data/tokenizers/punkt/PY3/science.pickle'),
    ]
    for dest in dests:
        parent, _ = os.path.split(dest)
        os.makedirs(parent, exist_ok=True)
        utila.log(dest)
        utila.file_replace_binary(dest, dumped)
    utila.log('done')
