# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def collect_and_replace(raw: str, pattern: list, verbose: bool = False) -> list:
    """Collect due list of pattern and avoids parsing items twice."""
    collected = []
    for method in pattern:
        parsed = method(raw, verbose=True)
        if not parsed:
            continue
        itemraw = parsed[0][1]
        # do not parse pattern twice
        raw = raw.replace(itemraw, '*' * len(itemraw))
        for item in parsed:
            if verbose:
                collected.append(item)
            else:
                collected.append(itemraw)
    return collected
