from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from maxflexsim.dsl.ast import (
    Assignment,
    BinaryOp,
    Call,
    Constraint,
    Declaration,
    Number,
    Program,
    Var,
)
from maxflexsim.ir.constraints import LatencyConstraint, LocalityConstraint
from maxflexsim.ir.graph import Graph
from maxflexsim.ir.oplib import OP_IMPLEMENTATIONS
from maxflexsim.ir.ops import Edge, Node
from maxflexsim.ir.types import I16, I32, DataType


@dataclass
class LoweringError(Exception):
    message: str


def _dtype_from_str(dtype: str) -> DataType:
    if dtype == "i16":
        return I16
    if dtype == "i32":
        return I32
    raise LoweringError(f"Unsupported dtype {dtype}")


def lower(program: Program) -> Graph:
    graph = Graph()
    declared: dict[str, DataType] = {}
    assignments: list[Assignment] = []
    constraints: list[Constraint] = []

    for stmt in program.statements:
        if isinstance(stmt, Declaration):
            dtype = _dtype_from_str(stmt.dtype)
            for name in stmt.names:
                declared[name] = dtype
        elif isinstance(stmt, Assignment):
            assignments.append(stmt)
        elif isinstance(stmt, Constraint):
            constraints.append(stmt)

    values: dict[str, str] = {}

    def ensure_input(name: str) -> str:
        if name not in declared:
            raise LoweringError(f"Undefined variable {name}")
        if name in values:
            return values[name]
        node_id = f"input_{name}"
        node = Node(
            id=node_id,
            op_type="INPUT",
            dtype=declared[name],
            shape=(),
            constraints=[],
            impl_choices=["input_small", "input_fast"],
            metadata={},
        )
        graph.add_node(node)
        values[name] = node_id
        return node_id

    def build_expr(expr) -> str:
        if isinstance(expr, Var):
            return ensure_input(expr.name)
        if isinstance(expr, Number):
            node_id = f"const_{len(graph.nodes)}"
            node = Node(
                id=node_id,
                op_type="CONST",
                dtype=I16,
                shape=(),
                constraints=[],
                impl_choices=[impl.name for impl in OP_IMPLEMENTATIONS["CONST"]],
                metadata={"value": expr.value},
            )
            graph.add_node(node)
            return node_id
        if isinstance(expr, BinaryOp):
            left_id = build_expr(expr.left)
            right_id = build_expr(expr.right)
            op_map = {"+": "ADD", "-": "ADD", "*": "MUL"}
            op_type = op_map[expr.op]
            node_id = f"{op_type.lower()}_{len(graph.nodes)}"
            node = Node(
                id=node_id,
                op_type=op_type,
                dtype=I16,
                shape=(),
                constraints=[],
                impl_choices=[impl.name for impl in OP_IMPLEMENTATIONS[op_type]],
                metadata={},
            )
            graph.add_node(node)
            graph.add_edge(
                Edge(
                    src=left_id,
                    dst=node_id,
                    bitwidth=16,
                    rate_bits_per_cycle=16.0,
                    latency_req=None,
                    metadata={},
                )
            )
            graph.add_edge(
                Edge(
                    src=right_id,
                    dst=node_id,
                    bitwidth=16,
                    rate_bits_per_cycle=16.0,
                    latency_req=None,
                    metadata={},
                )
            )
            return node_id
        if isinstance(expr, Call):
            op_type = expr.func.upper()
            if op_type not in OP_IMPLEMENTATIONS:
                raise LoweringError(f"Unsupported op {op_type}")
            node_id = f"{op_type.lower()}_{len(graph.nodes)}"
            node = Node(
                id=node_id,
                op_type=op_type,
                dtype=I16,
                shape=(),
                constraints=[],
                impl_choices=[impl.name for impl in OP_IMPLEMENTATIONS[op_type]],
                metadata={},
            )
            graph.add_node(node)
            for arg in expr.args:
                arg_id = build_expr(arg)
                graph.add_edge(
                    Edge(
                        src=arg_id,
                        dst=node_id,
                        bitwidth=16,
                        rate_bits_per_cycle=16.0,
                        latency_req=None,
                        metadata={},
                    )
                )
            return node_id
        raise LoweringError("Unsupported expression")

    for assignment in assignments:
        expr_id = build_expr(assignment.expr)
        out_id = f"output_{assignment.target}"
        dtype = declared.get(assignment.target, I16)
        node = Node(
            id=out_id,
            op_type="OUTPUT",
            dtype=dtype,
            shape=(),
            constraints=[],
            impl_choices=["output_small", "output_fast"],
            metadata={"symbol": assignment.target},
        )
        graph.add_node(node)
        graph.add_edge(
            Edge(
                src=expr_id,
                dst=out_id,
                bitwidth=dtype.bitwidth,
                rate_bits_per_cycle=16.0,
                latency_req=None,
                metadata={},
            )
        )
        values[assignment.target] = out_id

    _apply_constraints(graph, constraints)
    return graph


def _apply_constraints(graph: Graph, constraints: Iterable[Constraint]) -> None:
    for constraint in constraints:
        node_id = f"output_{constraint.target}"
        if node_id not in graph.nodes:
            raise LoweringError(f"Constraint targets unknown symbol {constraint.target}")
        node = graph.nodes[node_id]
        if constraint.kind == "latency":
            if not isinstance(constraint.value, float):
                raise LoweringError("Latency constraint must be numeric")
            node.constraints.append(LatencyConstraint(constraint.value))
        elif constraint.kind == "locality":
            node.constraints.append(LocalityConstraint(str(constraint.value)))
        else:
            raise LoweringError(f"Unsupported constraint {constraint.kind}")
