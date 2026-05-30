# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import utilo


@utilo.cacheme
def highnote_magic(text: str) -> str:
    """\
    >>> highnote_magic('ohnehin unmöglich.89 So')
    'ohnehin unmöglich. 89 So'
    """
    # highnote at the end of sentence
    text = re.sub(
        r'([a-z])([\.\!\?])(\d{1,4})([ ]{1,4})',
        r'\1\2 \3\4',
        text,
        flags=re.I,
    )
    return text
