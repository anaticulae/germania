#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""germania
======

The `germania` package is a wrapper for external tooling which have some
`magic` inside to determine the type of a word or split a text into
sentences into words.
"""

import importlib.metadata
import os

import analp
import ltk_data
import nltk

import germania.sentence
from germania.abbrev import find_abbrev
from germania.error.finding import TextError
from germania.error.finding import TextErrors
from germania.error.finding import TextErrorType
from germania.error.machine import TextErrorMachine
from germania.error.text import TextMachine
from germania.improve.abbreviation import abbreviation_magic
from germania.improve.highnote import highnote_magic
from germania.improve.href import href_magic
from germania.improve.magic import text_magic
from germania.language import LanguageResult
from germania.language import determine as lang
from germania.language import iseng
from germania.language import isfre
from germania.language import isger
from germania.magic import WordType
from germania.magic import WordTypes
from germania.magic import iscity
from germania.magic import isperson
from germania.magic import ispress
from germania.magic import isreference
from germania.magic import isyear
from germania.magic import wordtype
from germania.magic import wordtypes
from germania.pattern import matched
from germania.pattern.access import accessed
from germania.pattern.author import authors
from germania.pattern.author import authors_decide
from germania.pattern.book import bibtexts
from germania.pattern.book import doi
from germania.pattern.book import isbn
from germania.pattern.book import issn
from germania.pattern.book import references
from germania.pattern.book import volumes
from germania.pattern.date import dates
from germania.pattern.date import dates_master
from germania.pattern.date import dates_month_year
from germania.pattern.date import years
from germania.pattern.href import hyperlink
from germania.pattern.href import links
from germania.pattern.href import locallink
from germania.pattern.mail import mails
from germania.pattern.pagination import page_single
from germania.pattern.pagination import pagenumbers
from germania.pattern.pagination import pages_complex
from germania.quotation import extract_quotes
from germania.quotation import raw_quotation
from germania.sentence import Sentences
from germania.sentence import is_sentence
from germania.sentence import is_sentence_closed
from germania.sentence import sentence_select
from germania.sentence import sentence_tokenize
from germania.sentence import split_token
from germania.sequence import init
from germania.sequence import ngram
from germania.sequence import search
from germania.sequence import searches
from germania.sequence import token_plain
from germania.tagger import word_tag
from germania.text import words_fromstr
from germania.utils import collect_and_replace
from germania.utils.month import MONTH
from germania.utils.month import MONTH_REGEX
from germania.utils.month import month
from germania.word import Words
from germania.word import contain_quotation_marks
from germania.word import word_normalize
from germania.word import word_tokenize

split_words = word_tokenize  # pylint:disable=C0103
split_sentences = sentence_tokenize  # pylint:disable=C0103

__version__ = importlib.metadata.version('germania')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# REMOVE LATER
pages = page_single

nltk.download('crubadan', quiet=True)
nltk.download('punkt_tab', quiet=True)

# TODO: REMovE LATER
germania.sentence.language_select = lambda x: 'german'
