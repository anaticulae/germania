#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""german
======

The `german` package is a wrapper for external tooling which have some
`magic` inside to determine the type of a word or split a text into
sentences into words.
"""

import os

from german.headlines import HEADLINES
from german.headlines import isheadline
from german.language import LanguageResult
from german.language import determine as lang
from german.language import iseng
from german.language import isger
from german.magic import WordType
from german.magic import WordTypes
from german.magic import isperson
from german.magic import ispress
from german.magic import isreference
from german.magic import isyear
from german.magic import wordtype
from german.magic import wordtypes
from german.pattern import matched
from german.pattern.author import authors
from german.pattern.author import authors_decide
from german.pattern.date import dates
from german.pattern.date import years
from german.pattern.href import hyperlink
from german.pattern.mail import mails
from german.pattern.pagination import pagenumbers
from german.quotation import extract_quotes
from german.quotation import raw_quotation
from german.sentence import Sentences
from german.sentence import is_sentence
from german.sentence import is_sentence_closed
from german.sentence import split_sentences
from german.sentence import split_token
from german.sequence import init
from german.sequence import search
from german.sequence import searches
from german.text import words_fromstr
from german.word import Words
from german.word import contain_quotation_marks
from german.word import split_words

__version__ = '0.13.8'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
