# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import german_data


class LowerCasedSet:  # TODO: MOVE TO UTILA
    """\
    >>> data = LowerCasedSet('Helm melm GELM'.split())
    >>> assert 'HELM' in data
    >>> assert len(list(data)) == 3
    """

    def __init__(self, values):
        self.values = frozenset([item.lower() for item in values])

    def __iter__(self):
        return iter(self.values)

    def __contains__(self, item):
        return item.lower() in self.values

    def __or__(self, items):
        if isinstance(items, LowerCasedSet):
            items: frozenset = items.values
        return LowerCasedSet(self.values | items)


def load_dict(path) -> LowerCasedSet:
    assert os.path.exists(path), str(path)
    loaded = utila.file_read(path).splitlines()
    result = LowerCasedSet(loaded)
    return result


def load_data(path: str):
    if not os.path.exists(path):
        root = os.path.join(german_data.ROOT, 'german_data')
        path = os.path.join(root, path)
    return load_dict(path)
