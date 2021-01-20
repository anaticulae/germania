# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import german


def authors(raw: str):
    """\
    >>> authors('Becker, W.; Ulrich, P.; Botzkowski, T.; Eurich, S.')
    [['Becker', 'W.'], ['Ulrich', 'P.'], ['Botzkowski', 'T.'], ['Eurich', 'S.']]
    >>> authors('AASLID, R. - BRUBAKK, AO.')
    [['AASLID', 'R.'], ['BRUBAKK', 'AO.']]
    >>> authors('Beirness, D. and Vogel-Sprott, M.')
    [['Beirness', 'D.'], ['Vogel-Sprott', 'M.']]
    >>> authors('KUNCZIK, Michael/ZIPFEL, Astrid')
    [['KUNCZIK', 'Michael'], ['ZIPFEL', 'Astrid']]
    >>> authors('BOBEK H., FESL M.')
    [['BOBEK', 'H.'], ['FESL', 'M.']]
    >>> authors('HÖFER, Judith')
    [['HÖFER', 'Judith']]
    """
    raw = raw.strip()
    free = freeand(raw)
    semicolon = simple(raw)
    hyphen = simple(raw, extern='-', intern=',')
    slash = simple(raw, extern='/', intern=',')
    comma = simple(raw, extern=',', intern=' ')

    result = [free, semicolon, hyphen, slash, comma]
    balanced = [balance(item) for item in result]
    max_balance = maxindex(balanced)
    return result[max_balance]


def authors_decide(parsed: list) -> iamraw.Persons:
    result = []
    for author in parsed:
        result.append(judge(author))
    return result


def simple(raw: str, extern: str = ';', intern: str = ','):
    """\
    >>> simple('Becker, W.; Ulrich, P.')
    [['Becker', 'W.'], ['Ulrich', 'P.']]
    """
    result = []
    for item in raw.split(extern):
        result.append([it.strip() for it in item.split(intern) if it.strip()])
    return result


def freeand(raw: str):
    """\
    >>> freeand('Beirness, D. & Vogel-Sprott, M.')
    [['Beirness', 'D.'], ['Vogel-Sprott', 'M.']]
    """
    extracted = []
    try:
        # TODO: SOLVE `AND` PROBLEM ON OTHER PLACE?
        left, right = raw.split(' and ') if ' and ' in raw else raw.split('&')
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
    return result


def judge(parsed: list):
    if len(parsed) == 1:
        return iamraw.NoPerson(raw=parsed[0])  # pylint:disable=E1101
    raw = ' '.join(parsed)
    person = any([german.isperson(name) for name in parsed])
    if not person:
        return iamraw.NoPerson(raw=raw)  # pylint:disable=E1101
    name, firstname = decide_name(parsed)
    result = iamraw.Person(
        name=name,
        firstname=firstname,
        raw=raw,
    )
    return result


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
    if len(author) != 2:
        return False
    for item in author:
        if ';' in item:
            return False
        if ',' in item:
            return False
        if '/' in item:
            return False
    return True


def maxindex(items):
    if not items:
        return None
    current = 0
    for index, (value, count) in enumerate(items[1:], start=1):
        best = items[current][0]
        if value > best:
            current = index
        elif value == best:
            # equal values, use count as tie braker
            if count > items[current][1]:
                current = index
    return current
