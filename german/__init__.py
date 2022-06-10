#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import nltk_data

from german.error.finding import TextError
from german.error.finding import TextErrors
from german.error.finding import TextErrorType
from german.error.machine import TextErrorMachine
from german.error.text import TextMachine
from german.improve.abbreviation import abbreviation_magic
from german.improve.highnote import highnote_magic
from german.improve.href import href_magic
from german.improve.magic import text_magic
from german.language import LanguageResult
from german.language import determine as lang
from german.language import iseng
from german.language import isfre
from german.language import isger
from german.magic import WordType
from german.magic import WordTypes
from german.magic import iscity
from german.magic import isperson
from german.magic import ispress
from german.magic import isreference
from german.magic import isyear
from german.magic import wordtype
from german.magic import wordtypes
from german.pattern import matched
from german.pattern.access import accessed
from german.pattern.author import authors
from german.pattern.author import authors_decide
from german.pattern.book import doi
from german.pattern.book import isbn
from german.pattern.book import issn
from german.pattern.date import dates
from german.pattern.date import dates_master
from german.pattern.date import dates_month_year
from german.pattern.date import years
from german.pattern.href import hyperlink
from german.pattern.href import links
from german.pattern.href import locallink
from german.pattern.mail import mails
from german.pattern.pagination import pagenumbers
from german.pattern.pagination import pages
from german.pattern.pagination import pages_complex
from german.quotation import extract_quotes
from german.quotation import raw_quotation
from german.sentence import Sentences
from german.sentence import is_sentence
from german.sentence import is_sentence_closed
from german.sentence import sentence_select
from german.sentence import sentence_tokenize
from german.sentence import split_token
from german.sequence import init
from german.sequence import search
from german.sequence import searches
from german.tagger import word_tag
from german.text import words_fromstr
from german.utils.month import MONTH
from german.utils.month import MONTH_REGEX
from german.utils.month import month
from german.word import Words
from german.word import contain_quotation_marks
from german.word import word_normalize
from german.word import word_tokenize

split_words = word_tokenize  # pylint:disable=C0103
split_sentences = sentence_tokenize  # pylint:disable=C0103

__version__ = '1.21.4'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
