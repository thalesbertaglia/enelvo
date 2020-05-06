# -*- coding: utf-8 -*-
"""
Enelvo
~~~~~~~~~~~~~~~~~~~
A flexible normalizer for user-generated content.
:copyright: (c) 2017-2019 by Thales Bertaglia
:licence: MIT, see LICENSE for more details
"""
import logging

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__prog__ = "enelvo"
__title__ = "Enelvo"
__summary__ = "A flexible normaliser for user-generated content."
__uri__ = "https://www.github.com/tfcbertaglia/enelvo"
__author__ = "Thales Bertaglia"
__email__ = "contact@thalesbertaglia.com"

__license__ = "MIT"
__copyright__ = "Copyright 2017-2020 Thales Bertaglia"

# the user should dictate what happens when a logging event occurs
logging.getLogger(__name__).addHandler(logging.NullHandler())
