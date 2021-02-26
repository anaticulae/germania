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

import hugedata
import nltk.tokenize.punkt
import utila

import nltk_data
import science_text


def train(src: str, dest: str):
    utila.log(f'load corpus: {src}')

    if isinstance(src, list):
        content = [utila.file_read(item) for item in src]
        text = utila.NEWLINE.join(content)
    else:
        text = utila.file_read(src)
    # Make a new Tokenizer
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(train_text=text)

    utila.log(f'dump tokenizer: {dest}')
    dumped = pickle.dumps(tokenizer)
    utila.file_replace_binary(dest, dumped)


SOURCES = [
    hugedata.LIT_MASTER072,
    hugedata.LIT_MASTER075,
    hugedata.LIT_MASTER083,
    hugedata.LIT_MASTER089,
]

if __name__ == "__main__":
    tmp = utila.tmpfile(science_text.ROOT)
    train(SOURCES, tmp)

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
