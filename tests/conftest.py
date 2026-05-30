# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PATH = utilo.join(utilo.baw_root(__file__), 'train.py')

utilo.run(f'python {PATH}')
