# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hugedata

import science_text.train


def test_train(testdir):
    root = testdir.tmpdir
    sources = hugedata.RESOURCES[0:3]
    science_text.train.setup(root=root, source=sources)
