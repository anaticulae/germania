# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import german

MIXED = """\
James Grimmelmann (2008) bezeichnet die Offenbarung privater
Informationen in Social Media generell als Gefahr. Die Nutzer würden
allerdings die Privatheitsrisiken unterschätzen. Er vergleicht
Facebook-Nutzer mit so genannten Ghostridern, die ihr fahrendes Auto
verlassen und neben bzw. auf dem Fahrzeug tanzen, während es fahrerlos
weiterrollt: „[Facebook] users are the ones ghost riding the privacy
whip, dancing around on the roof as they expose their personal
information to the world”. Die Selbstdarstellung der Nutzer wird damit
als übertriebener Drang, sich der Welt zeigen zu wollen, geschildert und
als höchst gefährlich eingestuft.
"""

ENG = """\
„[Facebook] users are the ones ghost riding the privacy
whip, dancing around on the roof as they expose their personal
information to the world”
"""

SINGLE = """Die Nutzer würden allerdings die Privatheitsrisiken
unterschätzen."""

SINGLE_ENG = """„[…] participants are happy to disclose as much
information as possible to as many people as possible"""

MORE = """„Wohl nirgendwo sind so viel herzhafte Peinlichkeit und fröhliche
Entblößung zu finden wie in den sozialen Netzwerken des Internet. Die
Spaßvögel sind wie verhext von der Illusion, ganz unter sich zu sein.
"""


@pytest.mark.parametrize('source, expected', [
    pytest.param(MIXED, german.Language.GERMAN, id='mixed'),
    pytest.param(MORE, german.Language.GERMAN, id='more'),
    pytest.param(SINGLE, german.Language.GERMAN, id='single'),
    pytest.param(ENG, german.Language.ENGLISH, id='english'),
    pytest.param(SINGLE_ENG, german.Language.ENGLISH, id='single_eng'),
])
def test_language(source, expected):
    result = german.lang(source)
    assert result.language == expected, str(result)
