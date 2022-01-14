# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german

TEXT = """\
Es ist von „ Selbstentäußerung “ 32 , „ virtuellem Seelenstriptease “ 33 , „ Daten \
- Striptease im Web 2.0 “ 34 oder „ digitale [ m] Exhibitionismus “ 35 die Rede \
. Nutzer zeigten die Bereitschaft ,  36 . Privates werde öffentlich , Intimitäten \
einem unüberschaubaren Nutzerkreis mitgeteilt . Die WELT ( 26.10.2009 ) schreibt : \
„ In den Gemeinschaften des Web 2.0 schließt man Freundschaft per Mausklick , \
teilt man private Erlebnisse mit einem unübersehbaren Kreis von Fremden , gibt \
man öffentlich Auskunft über Sehnsüchte , den Pegelstand eigener Launen und \
das Schwanken der Gefühle . “ 37 Auch der SPIEGEL beschreibt eine ähnliche Situation :
"""
TOKENS = """\
„ In den Gemeinschaften des Web 2.0 schließt man Freundschaft per \
Mausklick , teilt Kreis \
von Fremden , gibt man öffentlich Auskunft über Sehnsüchte , den \
Pegelstand eigener Launen und das Schwanken der Gefühle. “
"""
EXPECTED = """\
„ In den Gemeinschaften des Web 2.0 schließt man Freundschaft per \
Mausklick , teilt man private Erlebnisse mit einem unübersehbaren Kreis \
von Fremden , gibt man öffentlich Auskunft über Sehnsüchte , den \
Pegelstand eigener Launen und das Schwanken der Gefühle . “\
"""


def test_sentence_select():
    """In TOKENS, in the middle, there are some missing token."""
    selected = german.sentence_select(TEXT, TOKENS)
    assert selected == EXPECTED
