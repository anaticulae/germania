# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Authors
=======

>>> authors('Becker, W.; Ulrich, P.; Botzkowski, T.; Eurich, S.')
[('Becker', 'W.'), ('Ulrich', 'P.'), ('Botzkowski', 'T.'), ('Eurich', 'S.')]

>>> authors('AASLID, R. - BRUBAKK, AO.')
[('AASLID', 'R.'), ('BRUBAKK', 'AO.')]

>>> authors('Beirness, D. and Vogel-Sprott, M.')
[('Beirness', 'D.'), ('Vogel-Sprott', 'M.')]

>>> authors('KUNCZIK, Michael/ZIPFEL, Astrid')
[('KUNCZIK', 'Michael'), ('ZIPFEL', 'Astrid')]

>>> authors('BOBEK H., FESL M.')
[('BOBEK', 'H.'), ('FESL', 'M.')]

>>> authors('HÖFER, Judith')
[('HÖFER', 'Judith')]

>>> authors('PEREIRA, M.G., VOLCHAN, E., SOUZA, G. G. DE, OLIVEIRA, '
... 'L., CAMPAGNOLI, R. R., PINHEIRO, W. M., & PESSOA, L. ')          # doctest: +NORMALIZE_WHITESPACE
[('PEREIRA', 'M.G.'), ('VOLCHAN', 'E.'), ('SOUZA', 'G. G. DE'), ('OLIVEIRA', 'L.'),
('CAMPAGNOLI', 'R. R.'), ('PINHEIRO', 'W. M.'), ('PESSOA', 'L.')]

>>> [author.name for author in authors_decide(authors('E. D’Andrea, P. Ducange'))]
['D’Andrea', 'Ducange']

>>> authors_decide(authors('S. Van Der Walt, S. C. Colbert, G. Varoquaux'))  # doctest: +NORMALIZE_WHITESPACE
[Person(name='Walt', firstname='S. Van Der',...Person(name='Colbert',
firstname='S. C.'...Person(name='Varoquaux', firstname='G.'...]

>>> authors('Deutsche Norm DIN 1422, Teil 1', verbose=True)
([('Deutsche', 'Norm', 'DIN', '1422'), ('Teil', '1')], 'Deutsche Norm DIN 1422, Teil 1')

If parsing only NoPersons we merge them to a single NoPerson
>>> authors_decide(*authors('Deutsche Norm DIN 1422, Teil 1', verbose=True))
[NoPerson(confidence=None, raw='Deutsche Norm DIN 1422, Teil 1')]

>>> authors('Lianos, Manuel/Hetzel, Rudolf')
[('Lianos', 'Manuel'), ('Hetzel', 'Rudolf')]

TODO: HOW TO IMPROVE THIS SITUATION?
>>> authors('Lianos, Manuel/Hetzel, Rudolf, Die Quadratur der Kreise. So arbeitet die FirmenLobby in Berlin')
[('Lianos', 'Manuel')]
"""

import functools
import re

import configo
import iamraw
import utila

import german


@functools.lru_cache(maxsize=4096)
def authors(raw: str, verbose: bool = False):
    """\
    >>> authors('M. Baccar,')
    [('M.', 'Baccar')]
    >>> authors('Hug, T. & Poscheschinik, G.')
    [('Hug', 'T.'), ('Poscheschinik', 'G.')]
    >>> authors('Hug, T. & Poscheschinik, G.', verbose=True)
    ([('Hug', 'T.'), ('Poscheschinik', 'G.')], 'Hug, T. & Poscheschinik, G.')
    """
    raw = raw.strip()
    free = freeand(raw)
    semicolon = simple(raw)
    hyphen = simple(raw, extern='-', intern=',')
    slash = simple(raw, extern='/', intern=',')
    comma = simple(raw, extern=',', intern=' ')
    # judge
    result = [free, semicolon, hyphen, slash, comma]
    balanced = [balance(item) for item in result]
    max_balance = maxindex(balanced)
    best = result[max_balance]
    # skip empty items as a result of empty `,` see: 'M. Baccar,'
    best = [tuple(item) for item in best if item]
    if verbose:
        # TODO: USE BEST MATCH ALGO TO DETERMINE SHORTEST RAW AREA
        best = (best, raw)
    return best


def authors_decide(parsed: list, raw: str = None) -> iamraw.Persons:
    """\
    >>> authors_decide([['Hug', 'T.'], ['Poscheschinik', 'G.']])
    [Person(name='Hug', firstname='T.',...Person(name='Poscheschinik',...ik G.')]
    """
    result = []
    for author in parsed:
        result.append(judge(author))
    if raw:
        # merge more than one NoPerson`s to a single NoPerson
        if all(isinstance(item, iamraw.NoPerson) for item in result):
            result = [iamraw.NoPerson(raw=raw)]
    return result


NAME_COUNT_MAX = configo.HV_INT_PLUS(default=7)


@functools.lru_cache(maxsize=4096)
def simple(raw: str, extern: str = ';', intern: str = ','):
    """\
    >>> simple('Becker, W.; Ulrich, P.')
    [('Becker', 'W.'), ('Ulrich', 'P.')]
    """
    result = []
    for item in raw.split(extern):
        parsed = tuple(it.strip() for it in item.split(intern) if it.strip())
        if any(len(names.split()) > NAME_COUNT_MAX for names in parsed):
            continue
        result.append(parsed)
    return result


@functools.lru_cache(maxsize=4096)
def freeand(raw: str):
    """\
    >>> freeand('Beirness, D. & Vogel-Sprott, M.')
    [('Beirness', 'D.'), ('Vogel-Sprott', 'M.')]

    garbage in garbage out, names are not separated correctly
    >>> freeand('Grunwald, Armin, Gerhard Banse, Christopher Coenen und Leonhard Hennen')
    [('Grunwald', 'Armin'), ('Gerhard Banse', 'Christopher Coenen'), ('Leonhard Hennen',)]
    """
    extracted = []
    try:
        left, right = splitand(raw)
        extracted.extend(left.split(','))
        extracted.extend(right.split(','))
    except ValueError:
        extracted.extend(raw.split(','))
    if not extracted:
        return None
    result = [[extracted[0]]]
    for item in extracted[1:]:
        item = item.strip()
        if not item:
            continue
        if len(result[-1]) == 1:
            result[-1].append(item)
        else:
            result.append([item])
    result = [tuple(item) for item in result]
    return result


@functools.lru_cache(maxsize=4096)
def splitand(raw: str):
    """\
    >>> splitand('ADM Arbeitskreis Deutscher Markt und Sozialforschungsinstitute e.V.')
    ['ADM Arbeitskreis Deutscher Markt und Sozialforschungsinstitute e.V.']
    >>> splitand('Bundesministerium der Justiz und für Verbraucherschutz')
    ['Bundesministerium der Justiz und für Verbraucherschutz']
    """
    if any(german.isperson(name) for name in raw.split()):
        raw = raw.replace(' and ', '&')
        raw = raw.replace(' und ', '&')
    return raw.split('&')


def judge(parsed: list):
    if len(parsed) == 1:
        return iamraw.NoPerson(raw=parsed[0])  # pylint:disable=E1101
    raw = ' '.join(parsed)
    noperson = german.magic.datums()[1]
    if any(item for item in parsed if item in noperson):
        return iamraw.NoPerson(raw=raw)
    if not person_simple(parsed):
        return iamraw.NoPerson(raw=raw)  # pylint:disable=E1101
    if any(utila.parse_numbers(name) for name in parsed):
        return iamraw.NoPerson(raw=raw)
    name, firstname = decide_name(parsed)
    result = iamraw.Person(
        name=name,
        firstname=firstname,
        raw=raw,
    )
    return result


VALID_NAME = re.compile(r'(\w\.|\w{4,})')


def person_simple(parsed: list, max_names: int = 4) -> bool:
    """\
    >>> person_simple('K. Fahrendholz'.split())
    True
    >>> person_simple('Boil C. G.'.split())
    True
    >>> person_simple('OHMEDA MEDIZINTECHNIK'.split())
    False
    >>> person_simple('Luhmann Niklas'.split())
    True
    >>> person_simple('E. D’Andrea'.split())
    True
    """
    if len(parsed) > max_names:
        return False
    if any(german.isperson(name) for name in parsed):
        return True
    if all(VALID_NAME.match(item) for item in parsed):
        # ensure that author contains `.` to fit in short `X. Name` pattern
        return '.' in ' '.join(parsed)
    return False


def decide_name(names: list) -> tuple:
    # TODO: NOT VERY SMART
    name = names[0]
    if '.' in name:
        name = utila.longest(names)
    firstname = ' '.join([item for item in names if item != name])
    return name, firstname


def balance(parsed_authors):
    if not parsed_authors:
        return None
    common = [valid_author(author) for author in parsed_authors]
    valid = len([item for item in common if item])
    ratio = valid / len(common)
    return ratio, len(common)


def valid_author(author):
    """\
    >>> valid_author(['S.', 'Van', 'Der', 'Walt'])
    True
    >>> valid_author(['S.', 'C.', 'Colbert'])
    True
    """
    if len(author) != 2:
        if len(author) > 2 and person_simple(author):
            return True
        return False
    for item in author:
        if ';' in item:
            return False
        if ',' in item:
            return False
        if '/' in item:
            return False
    return True


def maxindex(items) -> int:
    if not items:
        return None
    current = 0
    for index, content in enumerate(items[1:], start=1):
        if content is None:
            continue
        value, count = content
        best = items[current][0]
        if value > best:
            current = index
        elif value == best:
            # equal values, use count as tie braker
            if count > items[current][1]:
                current = index
    return current
