#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import nltk.data
import nltk_data
import utila

import german_data
import science_text.improve
import science_text.train


def setup_nltk():
    utila.log(f'NLTK: {nltk.data.path}\n')
    nltk.data.path.append(os.path.join(nltk_data.ROOT, 'nltk_data'))  # yapf:disable
    nltk.data.path.append(os.path.join(german_data.ROOT, 'german_data/nltk_data'))  # yapf:disable
    utila.log(f'NLTK: {nltk.data.path}\n')


if __name__ == "__main__":
    ROOT = science_text.ROOT
    utila.log(f'ROOT: {ROOT}')
    setup_nltk()
    utila.log('\nscience_text.train.setup')
    science_text.train.setup(ROOT)
    utila.log('\nscience_text.improve.setup')
    science_text.improve.setup(ROOT)
