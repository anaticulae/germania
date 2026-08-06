#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import pickle  # nosec
import sys

import hugedata
import konradus
import nltk.tokenize.punkt
import utilo

import germania_data
import science_text.config


def train(src: str, dest: str, verbose: bool = False):
    if isinstance(src, str):
        utilo.log(f'load corpus: {src}')
    else:
        for item in src:
            utilo.log(f'load corpus: {item}')

    if isinstance(src, list):
        content = [utilo.file_read(item) for item in src]
        text = utilo.NEWLINE.join(content)
    else:
        text = utilo.file_read(src)

    utilo.log('train tokenizer')
    utilo.log(f'use {len(text.splitlines())} lines')
    # Make a new Tokenizer
    lang_vars = science_text.config.SPunktLanguageVars()
    trainer = nltk.tokenize.punkt.PunktTrainer(lang_vars=lang_vars)
    trainer.train(text, verbose=verbose)

    trained = trainer.get_params()
    assert len(trained.abbrev_types) >= 20, len(trained.abbrev_types)
    assert len(trained.ortho_context) >= 20, len(trained.ortho_context)

    # add predefined abbreviations
    # remove last dot
    abbr = {item[0:-1] for item in konradus.ABBREVIATION_LOWER}
    utilo.debug(f'add predefined abbreviation:{abbr-trained.abbrev_types}')
    trained.abbrev_types = trained.abbrev_types | abbr

    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(
        train_text=trainer.get_params(),
        lang_vars=lang_vars,
    )

    utilo.log(f'dump tokenizer: {dest}')
    dumped = pickle.dumps(tokenizer)
    utilo.file_replace_binary(dest, dumped)


SOURCES = hugedata.RESOURCES


def setup(root, source=SOURCES):  # pylint:disable=W0102
    verbose = 'verbose' in sys.argv or '--verbose' in sys.argv

    tmp = utilo.tmpfile(germania_data.ROOT)
    train(source, tmp, verbose=verbose)

    dumped = utilo.file_read_binary(tmp)
    root = os.path.join(root, 'germania_data')
    dests = [
        os.path.join(root, 'nltk_data/tokenizers/punkt/science.pickle'),
        os.path.join(root, 'nltk_data/tokenizers/punkt/PY3/science.pickle'),
    ]
    for dest in dests:
        parent = utilo.path_parent(dest)
        os.makedirs(parent, exist_ok=True)
        utilo.log(dest)
        utilo.file_replace_binary(dest, dumped)
    utilo.log('done')


if __name__ == "__main__":  # pragma: no cover
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    setup(ROOT)
