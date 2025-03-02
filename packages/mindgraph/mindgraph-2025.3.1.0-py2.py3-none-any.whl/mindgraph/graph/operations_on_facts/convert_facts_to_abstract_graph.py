from typing import Dict, Tuple, Union, Optional, Literal, List
from datetime import datetime

def convert_facts_to_abstract_graph_dict(
    facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]], 
    direction: Optional[Literal['LR', 'RL', 'TB', 'BT']] = 'LR'
) -> Dict[str, Union[Dict[str, dict], List[Tuple[str, str, dict]]]]:
    """
    Converts facts to an abstract graph dictionary.
    Args:
        facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
        direction (Literal['LR', 'RL', 'TB', 'BT']): The direction of the graph.
    Returns:
        Dict[str, Union[Dict[str, dict], List[Tuple[str, str, dict]]]]
    """
    nodes_dict = {}
    edges_list = []
    for (_source_node, _target_node), _edges in facts.items():
        if len(_edges) == 0:
            continue

        if _source_node not in nodes_dict:
            # _source_node is node id as well as label
            nodes_dict[_source_node] = {'label': _source_node} # 'value', and 'style' are other possible keys
        if _target_node not in nodes_dict:
            nodes_dict[_target_node] = {'label': _target_node} # 'value', and 'style' are other possible keys
        
        for _edge, _facts in _edges.items():
            edge = (_source_node, _target_node, {'id': (_source_node, _target_node, _edge), 'label': _edge}) # 'value', and 'style' are other possible keys
            edges_list.append(edge)

    return {'nodes': nodes_dict, 'edges': edges_list, 'direction': direction}

def convert_facts_to_abstract_graph(
    facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]], 
    direction: Optional[Literal['LR', 'RL', 'TB', 'BT']] = 'LR', 
    **kwargs
) -> Union[Dict[str, Union[Dict[str, dict], List[Tuple[str, str, dict]]]], 'abstract.Graph']:
    """
    Converts facts to an abstract graph.
    Args:
        facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
        direction (Literal['LR', 'RL', 'TB', 'BT']): The direction of the graph.
        **kwargs: Additional keyword arguments.
    Returns:
        abstract.Graph
    """
    __graph__ = convert_facts_to_abstract_graph_dict(facts=facts, direction=direction, **kwargs)
    try:
        from abstract import Graph
        return Graph(__graph__)
    except ImportError:
        print("The abstract package is not installed. Please install it using `pip install abstract`.")
        return __graph__