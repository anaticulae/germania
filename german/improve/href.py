# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import re


@functools.lru_cache(maxsize=4096)
def href_magic(text: str) -> str:
    """\
    >>> href_magic('4. url: https : / / www . apache . org / licenses/LICENS')
    '4. url: https://www.apache.org/licenses/LICENS'
    """
    result = link_fink(text)
    return result


@functools.lru_cache(maxsize=4096)
def link_fink(text: str) -> str:
    """\
    >>> link_fink('url: http : / / www . bitkom . org / files / documents / BITKOM _ Leitfaden')
    'url: http://www.bitkom.org/files/documents/BITKOM_Leitfaden'
    """
    for (token, replacement) in SPACE_PATTERN:
        text = re.sub(token, replacement, text)
    return text


SPACE_PATTERN = (
    ('. org', '.org'),
    ('. de', '.de'),
    ('. com', '.com'),
    ('. net', '.net'),
    (' .org', '.org'),
    (' .de', '.de'),
    (' .com', '.com'),
    (' .net', '.net'),
    (' : /', ':/'),
    (' / ', '/'),
    (':/ ', ':/'),
    (' . ', '.'),
    (' _ ', '_'),
    ('_ ', '_'),
    ('/ ', '/'),
    ('http :', 'http:'),
    ('https :', 'https:'),
    ('http ://', 'http://'),
    ('https ://', 'https://'),
    ('http: //', 'http://'),
    ('https: //', 'https://'),
)
SPACE_PATTERN = [(re.escape(left), right) for left, right in SPACE_PATTERN]
SPACE_PATTERN.append((
    r'(?P<left>[a-z])\s{0,2}\.\s{0,2}(?P<right>[a-z])',
    r'\g<left>.\g<right>',
))
