import json
import math
from typing import Dict, List, Any, Optional

INPUT_JSON = """
    {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }
"""

class GraphNode:
    def __init__(self, children: List[int], parent: Optional[str]) -> None:
        self.children: List[int] = children
        self.parent: Optional[str] = parent
        self.relations: List[Optional[int]] = [0] * 5

    def __str__(self) -> str:
        return f"{self.children}, {self.parent}, {self.relations}"

def parse_json_to_dict(json_str: str) -> Dict[str, Any]:
    return json.loads(json_str)

def compute_entropy(matrix: List[List[int]]) -> float:
    if not matrix:
        return 0.0
    entropy_values = [0.0] * len(matrix[0])
    for row in matrix:
        for index, value in enumerate(row):
            if value == 0:
                continue
            probability = value / (len(row) - 1)
            entropy_values[index] -= probability * math.log2(probability)
    return sum(entropy_values)

def build_graph_structure(
    structure: Dict[str, Dict],
    adjacency: Dict[str, GraphNode],
    predecessor: Optional[str] = None
) -> None:
    for vertex, subtree in structure.items():
        descendants = []
        if isinstance(subtree, dict) and subtree:
            build_graph_structure(subtree, adjacency, vertex)
            descendants = list(subtree.keys())
        adjacency[vertex] = GraphNode(descendants, predecessor)
        adjacency[vertex].relations[0] = len(descendants)
        adjacency[vertex].relations[1] = 1 if predecessor else 0

def process_relations(adjacency: Dict[str, GraphNode]) -> None:
    for vertex, node in adjacency.items():
        if node.parent:
            parent_node = adjacency[node.parent]
            node.relations[4] += len(parent_node.children) - 1
            if parent_node.parent:
                node.relations[3] += 1
        for descendant in node.children:
            child_node = adjacency[str(descendant)]
            node.relations[2] += child_node.relations[2] + len(child_node.children)
            child_node.relations[3] += node.relations[3]

def main(input_data: str) -> None:
    graph_data = parse_json_to_dict(input_data)
    adjacency_representation = {}
    build_graph_structure(graph_data, adjacency_representation)
    process_relations(adjacency_representation)
    sorted_representation = dict(sorted(adjacency_representation.items(), key=lambda item: item[0]))
    for vertex, node in sorted_representation.items():
        print(f"{vertex}: {node.relations}")
    print(compute_entropy([node.relations for node in sorted_representation.values()]))

main(INPUT_JSON)
