# this_file: src/d361/__init__.py
"""
D361: Tools for Document360 content management.

This package provides modules for working with Document360 content.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("d361")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
