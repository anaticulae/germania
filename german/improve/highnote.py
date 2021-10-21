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
