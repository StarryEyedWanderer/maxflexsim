from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from maxflexsim.ir.ops import Edge, Node


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"Node {node.id} already exists")
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge.src not in self.nodes or edge.dst not in self.nodes:
            raise ValueError("Edge endpoints must exist in graph")
        self.edges.append(edge)

    def incoming(self, node_id: str) -> list[Edge]:
        return [edge for edge in self.edges if edge.dst == node_id]

    def outgoing(self, node_id: str) -> list[Edge]:
        return [edge for edge in self.edges if edge.src == node_id]

    def topological_order(self) -> list[str]:
        indegree = {node_id: 0 for node_id in self.nodes}
        for edge in self.edges:
            indegree[edge.dst] += 1
        queue = deque([node_id for node_id, deg in indegree.items() if deg == 0])
        order: list[str] = []
        while queue:
            node_id = queue.popleft()
            order.append(node_id)
            for edge in self.outgoing(node_id):
                indegree[edge.dst] -= 1
                if indegree[edge.dst] == 0:
                    queue.append(edge.dst)
        if len(order) != len(self.nodes):
            raise ValueError("Graph contains a cycle")
        return order

    def has_cycle(self) -> bool:
        try:
            self.topological_order()
        except ValueError:
            return True
        return False
