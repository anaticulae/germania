# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Do not change anything if both operation are used.

>>> unescape(unescape('Am 30. Juli habe ich Geburtstag.'))
'Am 30. Juli habe ich Geburtstag.'
"""

import utila

import german.utils.month


def escapes(text: str):
    """\
    >>> escapes('')
    ''
    """
    todo = utila.methods(utila.load_module(__file__), starts='ex_')
    for method in todo:
        text = method(text)
    return text


def unescape(text: str):
    """\
    >>> unescape('')
    ''
    """
    todo = utila.methods(utila.load_module(__file__), starts='un_')
    for method in todo:
        text = method(text)
    return text


DATE = utila.compiles(r"""
    \d{1,2}
    [ ]{0,5}
    \.
    [ ]{0,5}
    %s
""" % german.utils.month.MONTH_REGEX)

UN_DATE = utila.compiles(r"""
    \<\<\<DATE\:(.+?)\>\>\>
""")


def ex_date(text):
    r"""\
    >>> ex_date('vorgelegt, die am 21. Juni 2016  verabschiedet wurde')
    'vorgelegt, die am <<<DATE:21.\\WJuni>>> 2016  verabschiedet wurde'
    """

    def escape(match):
        result = match[0].replace(' ', r'\W')
        return f'<<<DATE:{result}>>>'

    return DATE.sub(escape, text)


def un_date(text):
    r"""\
    >>> un_date(r'vorgelegt, die am <<<DATE:21.\WJuni>>> 2016  verabschiedet wurde')
    'vorgelegt, die am 21. Juni 2016  verabschiedet wurde'
    """
    return UN_DATE.sub(r'\1', text).replace(r'\W', ' ')
