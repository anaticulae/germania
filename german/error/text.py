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
        \W
        (S\.)
        [ ]{0,4}\n?
        (?![\dixv\s])   # s. VII
    """)

    def check_pagenumber_complete(self, text: str) -> list:
        r"""\
        >>> check = TextMachine().check_pagenumber_complete
        >>> check('Bonn, Herford 1993, S.\nDer Brief')
        [TextError(...<TextErrorType.MISSING...raw='S.'...)]
        >>> check('Hier fehlt wohl S. die Seitennummer')
        [TextError(...<TextErrorType.MISSING...raw='S.'...)]
        >>> check('Schols. Hier')
        []
        >>> check('Berlin 19982, s. VII ')
        []
        """
        result = []
        for match in self.MISSING_PAGENUMBER.finditer(text):
            after = text[match.span()[1]:]
            if follows_name(after):
                continue
            error = german.TextError(
                state=german.TextErrorType.MISSING,
                location=self.location(match),
                raw=match[1],
            )
            result.append(error)
        return result


def follows_name(text: str) -> bool:
    """\
    >>> follows_name('Helmut wohnt hier')
    True
    >>> follows_name('Copyright (c) 2022 by Helmut')
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
