# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import nltk_data

from german_data.utils import load_data
from german_data.utils import load_dict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NLTK_DATA = os.path.join(ROOT, 'german_data/nltk_data')
# TODO: REPLACE WITH KNLP
nltk_data.add_nltk_path(NLTK_DATA)

# TODO: INTRODUCE LAZY LOADING
NAMES = load_data('names.dict')
PRESS = load_data('press.dict')
NOPERSON = load_data('noperson.dict')
INSTITUTION = load_data('institution.dict')
