# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from packaging.version import VERSION_PATTERN, Version

_VERSION_REGEX = re.compile(
    r"^\s*" + VERSION_PATTERN + r"\s*$", re.VERBOSE | re.IGNORECASE
)


def is_valid_version(version: str | None) -> bool:
    if not version:
        return False
    match = _VERSION_REGEX.search(version)
    return match is not None


def canonical_version(version: str | None) -> str | None:
    return Version(version).base_version if is_valid_version(version) else None  # type: ignore
