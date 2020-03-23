#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

from german.parser import words_fromstr
from german.sentence import is_sentence
from german.sentence import is_sentence_closed
from german.sentence import split_sentences
from german.word import Mark
from german.word import Marks
from german.word import Words
from german.word import split_words

__version__ = '0.0.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
