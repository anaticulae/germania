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

import nltk.data
import ltk_data
import utilo

import germania_data
import science_text.improve
import science_text.train


def setup_nltk():
    utilo.log(f'NLTK: {nltk.data.path}\n')
    nltk.data.path.append(os.path.join(ltk_data.ROOT, 'ltk_data'))  # yapf:disable
    nltk.data.path.append(os.path.join(germania_data.ROOT, 'germania_data/ltk_data'))  # yapf:disable
    utilo.log(f'NLTK: {nltk.data.path}\n')


def train():
    root = science_text.ROOT
    utilo.log(f'ROOT: {root}')
    setup_nltk()
    utilo.log('\nscience_text.train.setup')
    science_text.train.setup(root)
    utilo.log('\nscience_text.improve.setup')
    science_text.improve.setup(root)


if __name__ == "__main__":  # pragma: no cover
    train()
