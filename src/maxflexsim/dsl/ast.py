from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Program:
    statements: list[Statement]


class Statement:  # marker base
    pass


@dataclass(frozen=True)
class Declaration(Statement):
    names: list[str]
    dtype: str


@dataclass(frozen=True)
class Assignment(Statement):
    target: str
    expr: Expr


@dataclass(frozen=True)
class Constraint(Statement):
    kind: str
    target: str
    op: str
    value: object
    unit: str


class Expr:  # marker base
    pass


@dataclass(frozen=True)
class Var(Expr):
    name: str


@dataclass(frozen=True)
class Number(Expr):
    value: float


@dataclass(frozen=True)
class Call(Expr):
    func: str
    args: list[Expr]


@dataclass(frozen=True)
class BinaryOp(Expr):
    op: str
    left: Expr
    right: Expr
