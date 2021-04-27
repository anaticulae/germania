# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import nltk.data

from german_data.utils import load_data
from german_data.utils import load_dict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

NAMES = load_data('names.dict')
PRESS = load_data('press.dict')
NOPERSON = load_data('noperson.dict')
INSTITUTION = load_data('institution.dict')

nltk.data.path.insert(0, os.path.join(ROOT, 'german_data/nltk_data'))
