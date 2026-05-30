# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo

import germania_data


def load_dict(path) -> utilo.UpperCasedSet:
    assert os.path.exists(path), str(path)
    loaded = utilo.file_read(path).splitlines()
    result = utilo.UpperCasedSet(loaded)
    return result


def load_data(path: str):
    if not os.path.exists(path):
        root = os.path.join(germania_data.ROOT, 'germania_data')
        path = os.path.join(root, path)
    return load_dict(path)
