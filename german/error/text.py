# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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
            error = german.TextError(
                state=german.TextErrorType.MISSING,
                location=self.location(match),
                raw=match[1],
            )
            result.append(error)
        return result
