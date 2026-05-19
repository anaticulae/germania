# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import ltk_data

from germania_data.utils import load_data
from germania_data.utils import load_dict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NLTK_DATA = os.path.join(ROOT, 'germania_data/ltk_data')
# ensure that path exists, this is required to run data generator later
os.makedirs(NLTK_DATA, exist_ok=True)
# TODO: REPLACE WITH KNLP
ltk_data.add_nltk_path(NLTK_DATA)

# TODO: INTRODUCE LAZY LOADING
NAMES = load_data('names.dict')
PRESS = load_data('press.dict')
NOPERSON = load_data('noperson.dict')
INSTITUTION = load_data('institution.dict')
