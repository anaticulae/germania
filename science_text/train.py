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

import nltk.tokenize.punkt
import utila

import nltk_data
import science_text


def train(src: str, dest: str):
    utila.log(f'load corpus: {src}')

    text = utila.file_read(src)
    # Make a new Tokenizer
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(train_text=text)

    utila.log(f'dump tokenizer: {dest}')
    dumped = pickle.dumps(tokenizer)
    utila.file_replace_binary(dest, dumped)


if __name__ == "__main__":
    source = os.path.join(science_text.ROOT, 'science_text/data/science.plain')
    tmp = utila.tmpfile(science_text.ROOT)
    train(source, tmp)

    dumped = utila.file_read_binary(tmp)
    root = nltk_data.ROOT
    dests = [
        os.path.join(root, 'nltk_data/tokenizers/punkt/science.pickle'),
        os.path.join(root, 'nltk_data/tokenizers/punkt/PY3/science.pickle'),
    ]
    for dest in dests:
        utila.log(dest)
        utila.file_replace_binary(dest, dumped)
    utila.log('done')
