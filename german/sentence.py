# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import difflib
import functools

import configo
import knlp
import konrad
import utila

import german

Sentences = utila.Strings


@functools.lru_cache(maxsize=4096)
def sentence_tokenize(
    text: str,
    *,
    merge_divis: bool = True,
    normalize_newline: bool = True,
    normalize_spaces: bool = False,
) -> Sentences:  # pylint:disable=R1260,R0912
    r"""Split a regular `text` into sentence chunks.

    Args:
        text(str): text to split containing no newlines
        merge_divis(bool): merge lines with divis together
        normalize_newline(bool): replace newline with space single space
        normalize_spaces(bool): replace multiple spaces with single one
    Returns:
        list of splitted sentences

    # >>> sentence_tokenize('Dies ist der 1. Satz. Dies ist ein zweiter Satz!')
    ['Dies ist der 1. Satz.', 'Dies ist ein zweiter Satz!']
    >>> sentence_tokenize('Dieser Satz ent-\nhält eine Trennung.', merge_divis=True)
    ['Dieser Satz enthält eine Trennung.']
    >>> sentence_tokenize('Das  sind   eindeutig zu   viele Trennungen.', normalize_spaces=True)
    ['Das sind eindeutig zu viele Trennungen.']
    >>> sentence_tokenize('Der Stadtteil Berlin-\nNeuköln liegt im Süden von Berlin.')
    ['Der Stadtteil Berlin-Neuköln liegt im Süden von Berlin.']
    """
    text = utila.normalize_text(
        text,
        merge_divis=merge_divis,
        normalize_newline=normalize_newline,
        normalize_spaces=normalize_spaces,
    )
    # TODO: REMOVE LATER
    text = german.text_magic(text)
    language = language_select(text)
    # tokenize sentence
    tokenized = knlp.sent_tokenize(text, language=language)
    result = balance_sentence(tokenized)
    return result


@functools.lru_cache(maxsize=4096)
def language_select(text: str) -> str:
    if german.iseng(text):
        return 'science_english'
    return 'science'


def balance_sentence(sentences: list) -> list:
    """Merge neighbored unbalanced sentences."""
    # TODO: VERIFY IF THIS ALGO IMPROVES MERGING RESULT
    unbalenced = [
        index for index, item in enumerate(sentences) if quotation_count(item)
    ]
    # Determine groups of unbalanced sentences.
    grouped = utila.groupby_diff(unbalenced)

    def merge_group(group):
        if len(group) == 1:
            # merging single item is not required
            return sentences[group[0]]
        text = ' '.join([sentences[index] for index in group])
        return text

    merged = {group[0]: merge_group(group) for group in grouped}
    result = []
    for index, _ in enumerate(sentences):
        try:
            result.append(merged[index])
        except KeyError:
            if index in unbalenced:
                # already merge into other sentence
                continue
            result.append(sentences[index])
    return result


PAIR = '() []'.split()


@functools.lru_cache(maxsize=4096)
def isunbalanced(sentence: str) -> bool:
    """\
    >>> isunbalanced('I am ( unbalanced')
    True
    >>> isunbalanced('I am not ( unbalanced )')
    False
    """
    for start, close in PAIR:
        if sentence.count(start) != sentence.count(close):
            return True
    return False


def quotation_count(tokens: list) -> int:
    # TODO: MOVE TO KONRAD PACKAGE
    count = 0
    # TODO: CHECK DIFFERENT DOUBLE QUOTATION MARK SIGNS
    for token in tokens:
        count += token.count('„')
        count -= token.count('”')
        count -= token.count('“')
    return count


def open_quotation_mark(tokens: list) -> int:
    # TODO: MOVE TO KONRAD PACKAGE
    count = 0
    # TODO: CHECK DIFFERENT DOUBLE QUOTATION MARK SIGNS
    for token in tokens:
        count += token.count('„')
        count -= token.count('”')
        count -= token.count('“')
    return count > 0


QUOTATION_CLOSE_SIGNS = '"”“'  # TODO: REPLACE WITH KONRAD

SENTENCE_LENGTH_MIN = configo.HV_INT_PLUS(default=4)

SENTENCE_DOTS_MAX = configo.HV_PERCENT_PLUS(default=4.0)


@functools.lru_cache(maxsize=4096)
def is_sentence(
    sentence: str,
    min_length: int = SENTENCE_LENGTH_MIN,
    dots_percent_max=SENTENCE_DOTS_MAX,
) -> bool:
    length = len(sentence)
    if length < min_length:
        # sentence is too short
        return False
    dotcount = sentence.count('.')
    if dotcount >= 3:
        percent_sentence = dotcount / length
        if percent_sentence > dots_percent_max:
            # sentence contains too much dots, maybe a toc line
            return False
    splitted = sentence_tokenize(sentence)
    if len(splitted) > 1:
        return False
    token = split_token(splitted[0])
    if is_sentence_closed(token):
        return True
    return False


CLOSE_SIGNS = '.?!'


def is_sentence_closed(token: list) -> bool:  # pylint:disable=R0911
    """Check that the last character of the last token of a sentences contains
    a sentence close sign.

    >>> is_sentence_closed(['Effektivität', 'und', 'Effizienz.', '“'])
    True
    """
    assert token, 'empty sentence'
    assert isinstance(token, (list, tuple)), type(token)
    last = token[-1].strip()
    last_char = last[-1]
    if last_char in konrad.SIGN:
        # ... hello?
        return True
    if len(last) == 1:
        # 'Effizienz.', '“'
        if last not in QUOTATION_CLOSE_SIGNS:
            # TODO: CHECK ALL QUOTATION SIGNS?
            return False
    else:
        before_last_char = last[-2]
        if last_char in QUOTATION_CLOSE_SIGNS:
            # ... hello."
            if before_last_char in konrad.SIGN:
                return True
    if len(token) > 3:
        before_last = token[-2]
        third_last = token[-3]
        # HACK AND INCOMPLETE
        # greater than three cause a sentence needs some words
        # DOTTED, QUOTED
        # 'Effizienz.', '“'
        # TODO: SIMPLIFY THIS, USE PERMUTATION AND TOKEN CLASSES
        if last in QUOTATION_CLOSE_SIGNS and before_last[-1] in CLOSE_SIGNS:
            return True
        if before_last in QUOTATION_CLOSE_SIGNS and last[-1] in CLOSE_SIGNS:
            return True
        if last.isnumeric() and before_last in QUOTATION_CLOSE_SIGNS and third_last[-1] in CLOSE_SIGNS: # yapf:disable
            return True
        # DOTTED, QUOTED, NUMBER
        # 'Effizienz.', '“', '16'
    return False


@functools.lru_cache(maxsize=4096)
def split_token(text: str, normalize: bool = True):
    # replace text division -
    text = text.replace('-\n', '')
    # support multi line text
    text = text.replace('\n', ' ')
    tokens = text.split(' ')
    if normalize:
        tokens = [token for token in tokens if token]
    tokens = [split_special_chars(item) for item in tokens]
    tokens = utila.flatten(tokens)
    return tokens


SPECIAL = ['„', '“', '‘', '‚']


@functools.lru_cache(maxsize=4096)
def split_special_chars(token):
    """\
    >>> split_special_chars('„‚privat‘')
    ['„', '‚', 'privat', '‘']
    """
    for special in SPECIAL:
        splitted = token.split(special)
        token = f' {special} '.join(splitted)
    splitted = token.split()
    return splitted


def sentence_select(text: str, tokens: list, ratio_min: float = 0.5) -> str:  # pylint:disable=R0914
    """Select best matching sentence.

    Determine all possbile starts and ends and determine the most
    valueable sentence between.

    >>> sentence_select(text='Hier wohnt der; Helmut, sehr gerne.',
    ...                 tokens=' wohnt der ; Helmut , '.split())
    'wohnt der; Helmut,'
    """
    if isinstance(tokens, str):
        tokens = tokens.split()
    lang = german.lang(text)
    expected = ' '.join(konrad.mark2str(item, lang=lang) for item in tokens)
    # determine all possible starts and ends
    start, end = tokens[0], tokens[-1]
    starts = utila.findindex(text, konrad.mark2str(start, lang=lang))
    ends = utila.findindex(text, konrad.mark2str(end, lang=lang))
    if not start or not end:
        return None
    best = ''
    mostequal = 0.0
    for first, second in utila.starmap((starts, ends)):
        if second < first:
            continue
        sentence = text[first:second + 1]
        # spaces are handled as junk
        equal = difflib.SequenceMatcher(
            lambda x: x == " ",
            expected,
            sentence,
        )
        ratio = equal.ratio()
        if ratio < mostequal:
            continue
        # update best one
        best = sentence
        mostequal = ratio
    if mostequal < ratio_min:
        # matching is not good enough, do not return any result
        return None
    return best
