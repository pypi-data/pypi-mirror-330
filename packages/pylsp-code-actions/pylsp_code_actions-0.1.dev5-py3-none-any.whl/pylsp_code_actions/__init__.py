# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0
"""The pylsp_code_actions package."""
from importlib import metadata

try:
    __version__ = metadata.version("pylsp_code_actions")
except metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"
del metadata
