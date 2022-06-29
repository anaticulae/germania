# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import sdata
import utila

import german


class TextMachine(german.TextErrorMachine):

    MISSING_PAGENUMBER = utila.compiles(r"""
        (
            \s|
            [^\w]\.| # u.s.
            [,;:]
        )
        (
            S\.|
            p\.
        )
        [ ]{0,4}\n?
        (?![\dixv\s])   # s. VII
    """)

    def check_pagenumber_complete(self, text: str) -> list:
        r"""\
        >>> check = TextMachine().check_pagenumber_complete
        >>> check('Bonn, Herford 1993, S.\nDer Brief')
        [TextError(...<TextErrorType.MISSING...raw='S.'...)]
        >>> check('Hier fehlt wohlx S. die Seitennummer')
        [TextError(...<TextErrorType.MISSING...raw='S.'...)]
        >>> check('Vgl. Dixon, S.: Twitter: distribution of global audiences 2021')
        []
        >>> check('Schols. Hier')
        []
        >>> check('Berlin 19982, s. VII ')
        []
        >>> check('S. Meuschel, Legitimation und Parteiherrschaft ')
        []
        >>> check('in the U.S. | Pew Research')
        []
        >>> check('Meuschel S., Legitimation und Parteiherrschaft ')
        []

        run large text test
        >>> import backbone;check(backbone.text_improved(1024*1024))
        []
        """
        result = []
        for match in self.MISSING_PAGENUMBER.finditer(text):
            after = text[match.span()[1]:]
            if follows_name(after):
                continue
            start, lookback = match.span()[0], 60
            before = text[max(0, start - lookback):start]
            if name_before(before):
                continue
            error = german.TextError(
                state=german.TextErrorType.MISSING,
                location=self.location(match),
                raw=match[0].strip(),
            )
            result.append(error)
        return result


def follows_name(text: str) -> bool:
    """\
    >>> follows_name('Helmut wohnt hier')
    True
    >>> follows_name('Copyright (c) 2022 by Helmut')
    False
    >>> follows_name('Der Brief')
    False
    """
    text = text.strip()
    if re.match(r'^\w\.', text):
        return True
    for name in text.split()[0:4]:
        name = name.strip(':;, ')
        if sdata.isname(name):
            return True
    return False


def name_before(text: str) -> bool:
    """\
    >>> name_before('Legitimation und Parteiherrschaft Meuschel')
    True
    """
    token = text.rstrip(':;, ').rsplit(maxsplit=1)
    if not token:
        return False
    # select the right one
    name = token[-1].strip(':;, ')
    if sdata.isname(name):
        return True
    return False
