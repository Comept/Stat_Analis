import json
from typing import Dict, Any, Optional

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

def parse_json_to_dict(json_str: str) -> Dict[str, Any]:
    return json.loads(json_str)

def build_adjacency_data(
    node: Dict[str, Dict],
    adjacency: Dict[str, Any],
    ancestor: Optional[str] = None
) -> None:
    for vertex, subtree in node.items():
        offspring = []
        if isinstance(subtree, dict) and subtree:
            build_adjacency_data(subtree, adjacency, vertex)
            offspring = list(subtree.keys())
        adjacency[vertex] = [offspring, ancestor]

def execute_processing(json_input: str) -> None:
    graph_data = parse_json_to_dict(json_input)
    adjacency_repr = {}
    build_adjacency_data(graph_data, adjacency_repr)
    ordered_result = dict(sorted(adjacency_repr.items(), key=lambda item: item[0]))
    print(ordered_result)


execute_processing(INPUT_JSON)
