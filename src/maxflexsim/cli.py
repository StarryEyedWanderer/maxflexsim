from __future__ import annotations

import argparse
import sys

from maxflexsim.compiler.emit_certificate import emit_certificate
from maxflexsim.compiler.emit_config import emit_config
from maxflexsim.compiler.impl_select import select_impl
from maxflexsim.compiler.normalize import normalize
from maxflexsim.compiler.place import place
from maxflexsim.compiler.route_local import route
from maxflexsim.dsl.lower import LoweringError, lower
from maxflexsim.dsl.parser import parse_file
from maxflexsim.fabric.fabric import Fabric


def _compile(args: argparse.Namespace) -> int:
    try:
        fabric = Fabric.from_json(args.fabric)
        program = parse_file(args.input)
        graph = lower(program)
        graph = normalize(graph).graph
        graph = select_impl(graph).graph
        place(graph, fabric)
        routing = route(graph, fabric)
        emit_config(graph, fabric, args.output)
        emit_certificate(graph, fabric, routing.link_usage, args.output)
    except (ValueError, LoweringError) as exc:
        print(f"Compile failed: {exc}")
        return 1
    print(f"Compiled {args.input} for {fabric.name} -> {args.output}")
    print(f"Nodes: {len(graph.nodes)} Edges: {len(graph.edges)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="maxflex")
    sub = parser.add_subparsers(dest="command", required=True)
    compile_parser = sub.add_parser("compile", help="Compile DSL to config/certificate")
    compile_parser.add_argument("--fabric", required=True)
    compile_parser.add_argument("--in", dest="input", required=True)
    compile_parser.add_argument("--out", dest="output", required=True)
    compile_parser.set_defaults(func=_compile)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
