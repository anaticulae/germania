# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def flatten(lists, append: bool = False) -> list:
    """Chain lists of list to one list.

    Args:
        lists(iter): content to chain
        append(bool): if True do not raise TypeError if item is not iterable
    Returns:
        List of chained items
    Raises:
        TypeError: if append is False and item to chain is not iterable
    """
    result = []
    for item in lists:
        try:
            result.extend(item)
        except TypeError:
            if append:
                result.append(item)
            else:
                raise
    return result


utila.flatten = flatten
