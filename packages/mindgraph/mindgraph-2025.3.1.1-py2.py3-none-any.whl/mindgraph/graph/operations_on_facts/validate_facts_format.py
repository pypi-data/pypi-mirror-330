from typing import Dict, Tuple, Union, Optional, Literal
from datetime import datetime

def validate_facts_format(
    dictionary: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]],
    fact_id_starts_with: str = 'fact_',
    metadata_type: Literal['tuple', 'dictionary', 'either'] = 'either'
):
    """
    Validates the format of a dictionary of facts.
    Args:
        dictionary (Dict[Tuple[str, str], Dict[str, Dict]]): The dictionary of facts to validate.
        fact_id_starts_with (str): The prefix of the fact id.
    Returns:
        bool: True if the format is valid, False otherwise.
    """
    if not isinstance(dictionary, dict):
        raise TypeError(f"Dictionary is not a dictionary: {dictionary}")
    for key, edges_dict in dictionary.items():
        if len(key) != 2:
            raise TypeError(f"Key is not a tuple of length 2: {key} to be used as source_node, target_node")
        source_node, target_node = key
        if not isinstance(source_node, str):
            raise TypeError(f"Source node is not a string for edge {source_node} - {target_node}")
        if not isinstance(target_node, str):
            raise TypeError(f"Target node is not a string for edge {source_node} - {target_node}")
        if not isinstance(edges_dict, dict):
            raise TypeError(f"Edges are not a dictionary for edge {source_node} - {target_node}")
        if len(edges_dict) == 0:
            raise ValueError(f"Edges are empty for edge {source_node} - {target_node}")
        for edge, facts_as_dict in edges_dict.items():
            if not isinstance(edge, str):
                raise TypeError(f"Edge is not a string for edge {source_node} - {target_node}")
            if not isinstance(facts_as_dict, dict):
                raise TypeError(f"Facts is not a dictionary for edge {source_node} - {target_node} and edge {edge}: {facts_as_dict}")
            if len(facts_as_dict) == 0:
                raise ValueError(f"Facts are empty for edge {source_node} - {target_node} and edge {edge}")
            for fact_id, metadata in facts_as_dict.items():
                if not fact_id.startswith(fact_id_starts_with):
                    raise KeyError(f"Fact id {fact_id} does not start with {fact_id_starts_with} for edge {source_node} - {target_node} and edge {edge} with metadata: {metadata}")
                if metadata_type == 'either':
                    if not isinstance(metadata, (tuple, dict)):
                        raise TypeError(f"Metadata is not a tuple or dictionary for edge {source_node} - {target_node} and edge {edge} with fact id {fact_id}: {metadata}")
                elif metadata_type == 'tuple':
                    if not isinstance(metadata, tuple):
                        raise TypeError(f"Metadata is not a tuple for edge {source_node} - {target_node} and edge {edge} with fact id {fact_id}: {metadata}")
                elif metadata_type == 'dictionary':
                    if not isinstance(metadata, dict):
                        raise TypeError(f"Metadata is not a dictionary for edge {source_node} - {target_node} and edge {edge} with fact id {fact_id}: {metadata}")
    return True