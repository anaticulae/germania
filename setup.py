#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'germania',
    'germania.error',
    'germania.improve',
    'germania.pattern',
    'germania.sentence',
    'germania.utils',
    'germania_data',
    'science_text',
]

if __name__ == "__main__":  # pragma: no cover
    utila.install(
        __file__,
        include_package_data=True,
    )
    utila.log('train data')
    utila.run('python train.py')
