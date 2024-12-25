import json
from typing import Dict, Any, List, Optional

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
    def __init__(self, offspring: List[int], ancestor: Optional[str]) -> None:
        self.offspring: List[int] = offspring
        self.ancestor: Optional[str] = ancestor
        self.relationships: List[Optional[int]] = [0] * 5

    def __str__(self) -> str:
        return f"{self.offspring}, {self.ancestor}, {self.relationships}"

def convert_json_to_dict(json_data: str) -> Dict[str, Any]:
    return json.loads(json_data)

def analyze_graph(
    structure: Dict[str, Dict],
    adjacency: Dict[str, GraphNode],
    predecessor: Optional[str] = None
) -> None:
    for vertex, subtree in structure.items():
        descendants = []
        if isinstance(subtree, dict) and subtree:
            analyze_graph(subtree, adjacency, vertex)
            descendants = list(subtree.keys())
        adjacency[vertex] = GraphNode(descendants, predecessor)
        adjacency[vertex].relationships[0] = len(descendants)
        adjacency[vertex].relationships[1] = 1 if predecessor else 0

def calculate_relationships(adjacency: Dict[str, GraphNode]) -> None:
    for vertex, data in adjacency.items():
        if data.ancestor:
            parent = data.ancestor
            data.relationships[4] += len(adjacency[parent].offspring) - 1
            if adjacency[parent].ancestor:
                data.relationships[3] += 1
        for child in data.offspring:
            child_node = adjacency[str(child)]
            data.relationships[2] += child_node.relationships[2] + len(child_node.offspring)
            child_node.relationships[3] += data.relationships[3]

def execute(input_data: str) -> None:
    graph_structure = convert_json_to_dict(input_data)
    adjacency_representation = {}
    analyze_graph(graph_structure, adjacency_representation)
    calculate_relationships(adjacency_representation)
    sorted_representation = dict(sorted(adjacency_representation.items(), key=lambda item: item[0]))
    for vertex, node in sorted_representation.items():
        print(f"{vertex}: {node.relationships}")

execute(INPUT_JSON)
