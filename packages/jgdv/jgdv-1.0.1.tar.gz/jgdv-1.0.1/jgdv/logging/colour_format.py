#!/usr/bin/env python3
"""
see https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/
"""
# Imports:
from __future__ import annotations

# ##-- stdlib imports
import datetime
import enum
import functools as ftz
import itertools as itz
import logging
import logging as logmod
import pathlib as pl
import re
import warnings
from collections import defaultdict
from string import Formatter
from uuid import UUID, uuid1

# ##-- end stdlib imports

# ##-- 3rd party imports
import _string

try:
    # If `sty` is installed, use that
    # ##-- 3rd party imports
    from sty import bg, ef, fg, rs

    LEVEL_MAP    = defaultdict(lambda: rs.all)
    COLOUR_RESET = rs.all
    LEVEL_MAP.update({
        logging.DEBUG    : fg.grey,
        logging.INFO     : fg.blue,
        logging.WARNING  : fg.yellow,
        logging.ERROR    : fg.red,
        logging.CRITICAL : fg.red,
        "blue"           : fg.blue,
        "cyan"           : fg.cyan,
        "green"          : fg.green,
        "magenta"        : fg.magenta,
        "red"            : fg.red,
        "yellow"         : fg.yellow,
        "bg_blue"        : bg.blue,
        "bg_cyan"        : bg.cyan,
        "bg_green"       : bg.green,
        "bg_magenta"     : bg.magenta,
        "bg_red"         : bg.red,
        "bg_yellow"      : bg.yellow,
        "bold"           : ef.bold,
        "underline"      : ef.u,
        "italic"         : ef.italic,
        "RESET"          : rs.all
        })
except ImportError:
    # Otherwise don't add colours
    LEVEL_MAP    = defaultdict(lambda: "")
    COLOUR_RESET = ""

# ##-- end 3rd party imports

from jgdv import Proto, Mixin
from .stack_format import StackFormatter_m

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType
# Protocols:
from typing import Protocol, runtime_checkable
# Typing Decorators:
from typing import no_type_check, final, override, overload

if TYPE_CHECKING:
    from jgdv import Maybe
    from typing import Final
    from typing import ClassVar, Any, LiteralString
    from typing import Never, Self, Literal
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

##--|

# isort: on
# ##-- end types

class SimpleLogColour:
    """ Utility class for wrapping strings with specific colours """

    def __init__(self):
        raise TypeError("SimpleLogColour is Static, don't instance it")

    @staticmethod
    def green(s):
        return LEVEL_MAP['green'] + str(s) + COLOUR_RESET

    @staticmethod
    def blue(s):
        return LEVEL_MAP['cyan'] + str(s) + COLOUR_RESET

    @staticmethod
    def yellow(s):
        return LEVEL_MAP['yellow'] + str(s) + COLOUR_RESET

    @staticmethod
    def red(s):
        return LEVEL_MAP['red'] + str(s) + COLOUR_RESET

@Mixin(StackFormatter_m)
class ColourFormatter(logging.Formatter):
    """
    Stream Formatter for logging, enables use of colour sent to console

    Guarded Formatter for adding colour.
    Uses the sty module.
    If sty is missing, behaves as the default formatter class

    # Do *not* use for on filehandler
    Usage reminder:
    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(ColourFormatter(fmt))
    logger.addHandler(stdout_handler)
    """

    _default_fmt : ClassVar[str] = '{asctime} | {levelname:9} | {message}'
    _default_date_fmt : str      =  "%H:%M:%S"
    _default_style               = '{'

    def __init__(self, *, fmt=None, style=None):
        """
        Create the ColourFormatter with a given *Brace* style log format
        """
        super().__init__(fmt or self._default_fmt,
                         datefmt=self._default_date_fmt,
                         style=style or self._default_style)
        self.colours = LEVEL_MAP

    def format(self, record) -> str:
        if hasattr(record, "colour"):
            log_colour = self.colours[record.colour]
        else:
            log_colour = self.colours[record.levelno]

        return log_colour + super().format(record) + COLOUR_RESET

@Mixin(StackFormatter_m)
class StripColourFormatter(logging.Formatter):
    """
    Force Colour Command codes to be stripped out of a string.
    Useful for when you redirect printed strings with colour
    to a file
    """

    _default_fmt         = "{asctime} | {levelname:9} | {shortname:25} | {message}"
    _default_date_fmt    = "%Y-%m-%d %H:%M:%S"
    _default_style       = '{'
    _colour_strip_re     = re.compile(r'\x1b\[([\d;]+)m?')

    def __init__(self, *, fmt=None, style=None):
        """
        Create the StripColourFormatter with a given *Brace* style log format
        """
        super().__init__(fmt or self._default_fmt,
                         datefmt=style or self._default_date_fmt,
                         style=self._default_style)

    def format(self, record) -> str:
        result    = super().format(record)
        no_colour = self._colour_strip_re.sub("", result)
        return no_colour
