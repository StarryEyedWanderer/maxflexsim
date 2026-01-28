from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from maxflexsim.dsl.ast import (
    Assignment,
    BinaryOp,
    Call,
    Constraint,
    Declaration,
    Number,
    Program,
    Statement,
    Var,
)


@dataclass
class Token:
    kind: str
    value: str


_TOKEN_REGEX = re.compile(
    r"(?P<NUMBER>\d+(?:\.\d+)?)|(?P<NAME>[A-Za-z_][A-Za-z0-9_]*)|(?P<SYM>==|<=|[()+\-*/,:@=])"
)


class _Tokenizer:
    def __init__(self, text: str) -> None:
        self.tokens = [
            Token(kind=match.lastgroup or "", value=match.group(0))
            for match in _TOKEN_REGEX.finditer(text)
        ]
        self.position = 0

    def peek(self) -> Token | None:
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def next(self) -> Token:
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected end of input")
        self.position += 1
        return token

    def expect(self, kind: str, value: str | None = None) -> Token:
        token = self.next()
        if token.kind != kind or (value is not None and token.value != value):
            raise ValueError(f"Expected {kind} {value}, got {token.kind} {token.value}")
        return token


class _ExpressionParser:
    def __init__(self, tokenizer: _Tokenizer) -> None:
        self.tokens = tokenizer

    def parse_expr(self):
        node = self.parse_term()
        while True:
            token = self.tokens.peek()
            if token and token.kind == "SYM" and token.value in {"+", "-"}:
                op = self.tokens.next().value
                right = self.parse_term()
                node = BinaryOp(op=op, left=node, right=right)
            else:
                break
        return node

    def parse_term(self):
        node = self.parse_factor()
        while True:
            token = self.tokens.peek()
            if token and token.kind == "SYM" and token.value == "*":
                self.tokens.next()
                right = self.parse_factor()
                node = BinaryOp(op="*", left=node, right=right)
            else:
                break
        return node

    def parse_factor(self):
        token = self.tokens.peek()
        if token is None:
            raise ValueError("Unexpected end of input")
        if token.kind == "NUMBER":
            self.tokens.next()
            return Number(value=float(token.value))
        if token.kind == "NAME":
            name = self.tokens.next().value
            if self.tokens.peek() and self.tokens.peek().value == "(":
                self.tokens.next()
                args = []
                if self.tokens.peek() and self.tokens.peek().value != ")":
                    args.append(self.parse_expr())
                    while self.tokens.peek() and self.tokens.peek().value == ",":
                        self.tokens.next()
                        args.append(self.parse_expr())
                self.tokens.expect("SYM", ")")
                return Call(func=name, args=args)
            return Var(name=name)
        if token.kind == "SYM" and token.value == "(":
            self.tokens.next()
            node = self.parse_expr()
            self.tokens.expect("SYM", ")")
            return node
        raise ValueError(f"Unexpected token {token.kind} {token.value}")


def parse(source: str) -> Program:
    statements: list[Statement] = []
    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("@"):
            match = re.match(
                r"@(?P<kind>\w+)\((?P<target>\w+)\)\s*<=\s*(?P<value>\w+)\s*(?P<unit>\w*)",
                line,
            )
            if not match:
                raise ValueError(f"Invalid constraint: {line}")
            value_text = match.group("value")
            value: object
            if re.match(r"^\d+(?:\.\d+)?$", value_text):
                value = float(value_text)
            else:
                value = value_text
            statements.append(
                Constraint(
                    kind=match.group("kind"),
                    target=match.group("target"),
                    op="<=",
                    value=value,
                    unit=match.group("unit"),
                )
            )
            continue
        if ":" in line and "=" not in line:
            names_part, dtype = [part.strip() for part in line.split(":", 1)]
            names = [name.strip() for name in names_part.split(",")]
            statements.append(Declaration(names=names, dtype=dtype))
            continue
        if "=" in line:
            target, expr_text = [part.strip() for part in line.split("=", 1)]
            tokenizer = _Tokenizer(expr_text)
            expr = _ExpressionParser(tokenizer).parse_expr()
            statements.append(Assignment(target=target, expr=expr))
            continue
        raise ValueError(f"Unrecognized statement: {line}")
    return Program(statements=statements)


def parse_file(path: str | Path) -> Program:
    return parse(Path(path).read_text(encoding="utf-8"))
