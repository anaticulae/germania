# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import konradus
import utilo


@utilo.cacheme
def abbreviation_magic(text: str) -> str:
    """\
    >>> abbreviation_magic('Helmut hier u. a. und mehr.')
    'Helmut hier u.a. und mehr.'
    >>> abbreviation_magic('a. a. o.')
    'a.a.o.'
    """
    for token, replace in TEXT_MAGIC:
        text = text.replace(token, replace)
    return text


TEXT_MAGIC = [
    ('. '.join(item.split('.')).strip(), item)
    for item in list(konradus.ABBREVIATION) + list(konradus.ABBREVIATION_LOWER)
    if item.count('.') > 1
]
