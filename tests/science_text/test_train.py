# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hugedata
import utila

import science_text.train
import science_text.improve


def test_train(testdir):
    root = testdir.tmpdir
    sources = hugedata.RESOURCES[0:3]
    science_text.train.setup(root=root, source=sources)
    current = utila.file_count(root)
    assert current == 2


def test_improve(testdir):
    root = testdir.tmpdir
    science_text.improve.setup(root)
    current = utila.file_count(root)
    assert current == 2
