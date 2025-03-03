#!/usr/bin/env python3
"""
Types that help add clarity

Provides a number of type aliases and shorthands.
Such as `Weak[T]` for a weakref, `Stack[T]`, `Queue[T]` etc for lists,
and `Maybe[T]`, `Result[T, E]`, `Either[L, R]`.

"""

# Imports:
from __future__ import annotations

from types import UnionType, GenericAlias, MethodType, LambdaType
from typing import (Any, Callable, Generator, Never, TypeGuard, Self)
from uuid import UUID, uuid1
from re import Pattern, Match
import datetime
from weakref import ref
from jgdv._abstract import protocols

type VerStr                   = str # A Version String
type Ident                    = str # Unique Identifier Strings
type FmtStr                   = str # Format Strings like 'blah {val} bloo'
type FmtSpec                  = str # Format and conversion parameters. eg: 'blah {val:<9!r}' would be ':<10!r'
type FmtKey                   = str # Names of Keys in a FmtStr
type Rx                       = Pattern
type RxMatch                  = Match
type RxStr                    = str
type Ctor[T]                  = type[T] | Callable[[*Any], T]
type Func[I,O]                = Callable[I,O]
type Method[I,O]              = MethodType[type, I,O]
type Decorator                = Func[[Func],Func]
type Lambda                   = LambdaType

# Containers:
type Weak[T]                  = ref[T]
type Stack[T]                 = list[T]
type Fifo[T]                  = list[T]
type Queue[T]                 = list[T]
type Lifo[T]                  = list[T]
type Vector[T]                = list[T]
type Mut[T]                   = T
type NoMut[T]                 = T

type Maybe[T]                 = T | None
type Result[T, E:Exception]   = T | E
type Either[L, R]             = L | R
type SubOf[T]                 = TypeGuard[T]

# Shorthands
type M_[T]                    = T | None
type R_[T, E:Exception]       = T | E
type E_[L, R]                 = L | R

# TODO : Make These subtypes of int that are 0<=x
type Depth              = int
type Seconds            = int


type DateTime           = datetime.datetime
type TimeDelta          = datetime.timedelta

type CHECKTYPE          = Maybe[type|GenericAlias|UnionType]

type DictKeys           = type({}.keys())
type DictItems          = type({}.items())
type DictVals           = type({}.values())


# TODO: traceback and code types
