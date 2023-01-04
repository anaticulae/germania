# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konrad
import utila

import german

Words = list[str]


def word_tokenize(
    items: str,
    validate_sentences: bool = True,
    token_normalize: bool = False,
    lang: konrad.Language = None,
) -> Words:
    """\
    >>> word_tokenize('•Wie gestaltet sich die Anreise der Kunden?')
    [<Mark.LIST_DOT:...>, 'Wie', 'gestaltet',...<Mark.QUESTION_MARK:...>]
    >>> word_tokenize('Systemen“{{hn:144:nh}}. Sie!', validate_sentences=False)
    ['Systemen', <Mark.QUOTATION_MARK_DOUBLE_CLOSE: 33>, '{{hn:144:nh}}', <Mark.FULLSTOP: 22>...]
    >>> word_tokenize('Mister-Dinh', validate_sentences=False)
    ['Mister', <Mark.HYPHEN: 23>, 'Dinh']
    >>> word_tokenize('mit 38 % höheren Click-Through-Raten als andere Bilder', validate_sentences=False)
    ['mit', '38', <Mark.PERCENT: 43>, 'höheren', 'Click', <Mark.HYPHEN: 23>, 'Through', <Mark.HYPHEN: 23>...]
    """
    if validate_sentences and not german.is_sentence(items):
        # Ensure to parse complete sentences.
        return None
    items = items.replace('\n', ' ')
    items = items.replace(' z. B. ', ' z.B. ')
    result = []
    current = []
    for index, char in enumerate(items):
        if char == ' ':
            handle_whitespace(result, current)
            continue
        try:
            special = konrad.matches(char, lang=lang)
        except KeyError:
            # append normal text char or number
            current.append(char)
        else:
            handle_token(result, items, current, index, char, special)
    if current:
        if items[-1] in konrad.SIGN or not validate_sentences:
            result.append(''.join(current))
            current = []
    assert not current or validate_sentences, current
    result = unplug_numbers(result)
    result = merge_numbers(result, items)
    result = merge_reference(result, items)
    result = merge_highnote(result)
    if token_normalize:
        result = [
            word_normalize(item) if isinstance(item, str) else item
            for item in result
        ]
    return result


def word_normalize(item: str, lang: str = 'ger') -> str:
    """\
    >>> word_normalize('Eisenbahnen')
    'eisenbahn'
    >>> word_normalize('Eisenbahnen Eisenbahnen Eisenbahnen')
    'eisenbahn eisenbahn eisenbahn'
    """
    stemmer = stemmer_load(lang=lang)
    if ' ' in item:
        return ' '.join(word_normalize(it) for it in item.split())
    return stemmer.stem(item)


def handle_whitespace(result, current):
    if len(current) == 1:
        if utila.isnumber(current[0]):
            # number and space '5 '
            result.append(current[0])
            current.clear()
        return
    if len(current) >= 2:
        result.append(''.join(current))
        current.clear()


def handle_token(result, items, current, index, token, special):
    # evaluate sentence sign
    if dot_pattern(current, token):
        current.append(token)
        return
    if number_bracket_pattern(current, token):
        result.append(''.join(current))
        result.append(special)
        current.clear()
        # current.append(token)
        return
    if dotable_shortcut_pattern(current, token):
        current.append(token)  # TODO: REPLACE WITH SINGLE DOT
        if index != (len(items) - 1):
            return
    if len(current) >= 2:
        result.append(''.join(current))
        current.clear()
    if len(current) == 1 and utila.isnumber(current[0]):
        # Number SpecialChar 4. 2,
        result.append(current[0])
        result.append(special)
        current.clear()
        return
    # append ), ], 3., etc.
    result.append(special)


def merge_numbers(result, source) -> list:
    """\
    >>> merge_numbers(['Ich', '134', konrad.Mark.FULLSTOP, '456', 'kg'], 'Ich 134.456 kg')
    ['Ich', '134.456', 'kg']
    """
    if len(result) <= 2:
        return result
    merged = result[:2]
    for item in result[2:]:
        if not utila.isnumber(item):
            merged.append(item)
            continue
        if merged[-1] == konrad.Mark.FULLSTOP and utila.isnumber(merged[-2]):
            together = f'{merged[-2]}.{item}'
            if together not in source:
                merged.append(item)
            else:
                merged = merged[:-2] + [together]
        else:
            merged.append(item)
    return merged


def merge_reference(result, source) -> list:
    """\
    >>> merge_reference(['Punkt', '3.2', konrad.Mark.FULLSTOP, 'Helm'], 'Punkt 3.2. Helm')
    ['Punkt', '3.2.', 'Helm']
    """
    if len(result) <= 1:
        return result
    merged = result[:1]
    for item in result[1:]:
        if item != konrad.Mark.FULLSTOP and not utila.isnumber(item):
            merged.append(item)
            continue
        if not german.isreference(merged[-1]):
            merged.append(item)
            continue
        if item == konrad.Mark.FULLSTOP:
            together = f'{merged[-1]}.'
        else:
            together = f'{merged[-1]}{item}'
        if together in source:
            merged[-1] = together
        else:
            merged.append(item)
    return merged


class MergeAutomata:

    def __init__(self, pattern, replace: callable):
        self.pattern = pattern
        self.replace = replace
        self.buffer = []
        self.result = []

    def put(self, item):
        self.buffer.append(item)
        if self.match is None:
            # not long enough
            return
        if self.match is False:  # pylint:disable=compare-to-zero
            self.result.append(self.buffer[0])
            self.buffer = self.buffer[1:]
            return
        replaced = self.replace(self.buffer)
        self.result.append(replaced)
        self.buffer.clear()

    @property
    def match(self) -> bool:
        if len(self.buffer) < len(self.pattern):
            return None
        for current, expected in zip(self.buffer, self.pattern):
            if isinstance(expected, (str, konrad.Mark)):
                if current != expected:
                    return False
                continue
            if isinstance(current, konrad.Mark):
                return False
            if not expected.match(current):
                return False
        return True

    def end(self) -> list:
        self.result.extend(self.buffer)
        result = list(self.result)
        self.result.clear()
        self.buffer.clear()
        return result


def merge_highnote(items) -> list:
    highnote = MergeAutomata(
        pattern=(
            konrad.Mark.BRACKET_ELEPHANT_OPEN,
            konrad.Mark.BRACKET_ELEPHANT_OPEN,
            'hn',
            konrad.Mark.COLON,
            utila.compiles(r'\d{1,4}'),
            konrad.Mark.COLON,
            'nh',
            konrad.Mark.BRACKET_ELEPHANT_CLOSE,
            konrad.Mark.BRACKET_ELEPHANT_CLOSE,
        ),
        replace=lambda x: '{{hn:%s:nh}}' % x[4],
    )
    for item in items:
        highnote.put(item)
    result = highnote.end()
    return result


UNPLUG_NUMBERS = utila.compiles(r'(\d{1,10})')


def unplug_numbers(result):
    """\
    >>> unplug_numbers(['Hier', 'ABC134', 'S.', '32ff'])
    ['Hier', 'ABC', '134', 'S.', '32', 'ff']
    """
    result = [
        UNPLUG_NUMBERS.split(item) if isinstance(item, str) else item
        for item in result
    ]
    result = utila.flat(result, append=True)  # pylint:disable=unexpected-keyword-arg
    result = utila.notempty(result)  # pylint:disable=E1101
    return result


def dot_pattern(current, char) -> bool:
    """\
    >>> dot_pattern(['1'], ')')
    False
    >>> dot_pattern(['3', '.', '2'], '.')
    False
    """
    # W.D.
    if len(current) == 1:
        if current[0].isnumeric():
            # 1) # TODO: VERIFY THIS COMMENT
            return False
        if current[0] not in ')]':
            return True
    if len(current) == 3 and char == '.' and current[1] == '.':
        if utila.isnumber(current[0]) and utila.isnumber(current[2]):
            # 3.2
            return False
        return True
    return False


def number_bracket_pattern(current, char) -> bool:
    """\
    >>> number_bracket_pattern(['1', '2', '3'], ')')
    True
    """
    current = ''.join(current).lower()
    if not current.isnumeric():
        return False
    if char in '])}':
        return True
    return False


def dotable_shortcut_pattern(current, char) -> bool:
    if char != '.':
        return False
    current = ''.join(current).lower() + char
    return current in konrad.ABBREVIATION_LOWER


MARKS = (
    konrad.Mark.QUOTATION_MARK,
    konrad.Mark.QUOTATION_MARK_DOUBLE_CLOSE,
    konrad.Mark.QUOTATION_MARK_DOUBLE_OPEN,
    konrad.Mark.QUOTATION_MARK_SINGLE_CLOSE,
    konrad.Mark.QUOTATION_MARK_SINGLE_OPEN,
)


def contain_quotation_marks(items) -> bool:
    """\
    >>> contain_quotation_marks(['Helm', 'Schelm', 1334, konrad.Mark.QUOTATION_MARK])
    True
    >>> contain_quotation_marks((123, 'Helm'))
    False
    """
    return any(item in MARKS for item in items)


@utila.cacheme
def stemmer_load(lang: str = 'ger'):  # pylint:disable=W0613
    import nltk.stem
    lang = konrad.complexlang(lang)
    result = nltk.stem.SnowballStemmer(language=lang)
    return result
