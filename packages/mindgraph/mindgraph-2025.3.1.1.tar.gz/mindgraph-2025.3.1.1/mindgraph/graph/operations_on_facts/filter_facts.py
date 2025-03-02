from typing import Dict, Tuple, Union, Optional, List
from datetime import datetime

def filter_facts(
    facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]], 
    subject: Optional[str] = None,
    predicate: Optional[str] = None,
    object: Optional[str] = None,
    fact_id: Optional[str] = None,
    fact_source: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None, 
    fields: Optional[Union[Tuple[str, ...], List[str]]] = ('fact_id', 'fact_source', 'timestamp', 'depth')
) -> bool:
    """
    Filters the facts dictionary.
    Args:
        facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to check.
        subject (Optional[str]): The subject of the fact.
        predicate (Optional[str]): The predicate of the fact.
        object (Optional[str]): The object of the fact.
        fact_id (Optional[str]): The fact_id of the fact.
        fact_source (Optional[str]): The fact_source of the fact.
        start_time (Optional[datetime]): The start_time of the fact.
        end_time (Optional[datetime]): The end_time of the fact.
        fields (Optional[Union[Tuple[str, ...], List[str]]]): The fields to filter by.
    Returns:
        Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]: The filtered facts.
    """

    # filter by subject and object

    def _filter_by_fact_id_and_fact_source_and_timestamp(
        metadata: Union[Tuple, Dict]
    ) -> dict:
        
        if isinstance(metadata, tuple):
            fact_id_index = fields.index('fact_id')
            fact_source_index = fields.index('fact_source')
            timestamp_index = fields.index('timestamp')
            _fact_id = metadata[fact_id_index]
            _fact_source = metadata[fact_source_index]
            _timestamp = metadata[timestamp_index]

            if fact_id is not None and _fact_id != fact_id:
                return None
            if fact_source is not None and _fact_source != fact_source:
                return None
            if start_time is not None and _timestamp is not None and _timestamp < start_time:
                return None
            if end_time is not None and _timestamp is not None and _timestamp > end_time:
                return None
        return metadata.copy()
    
    def _filter_by_fact_id(facts_as_dict: Dict[str, Union[Tuple, Dict]]) -> Dict[str, Union[Tuple, Dict]]:
        if fact_id is None:
            new_facts_as_dict = {}
            for _fact_id, _metadata in facts_as_dict.items():
                metadata = _filter_by_fact_id_and_fact_source_and_timestamp(_metadata)
                if metadata is not None:
                    new_facts_as_dict[_fact_id] = metadata
            return new_facts_as_dict
        else:
            one_metadata = _filter_by_fact_id_and_fact_source_and_timestamp(facts_as_dict[fact_id])
            if one_metadata is not None:
                return {fact_id: one_metadata}
            else:
                return None
    
    def _filter_by_predicate(edges: Dict[str, Dict[str, Union[Tuple, Dict]]]) -> Dict[str, Dict[str, Union[Tuple, Dict]]]:
        if predicate is None:
            new_edges = {}
            for _edge, _facts_as_dict in edges.items():
                facts_as_dict = _filter_by_fact_id(_facts_as_dict)
                if facts_as_dict is not None:
                    new_edges[_edge] = facts_as_dict
            if len(new_edges) == 0:
                return None
            return new_edges
        else:
            if predicate in edges:
                one_edge = edges[predicate]
                one_edge = _filter_by_fact_id(one_edge)
                if one_edge is not None:
                    return {predicate: one_edge}
                else:
                    return None
            else:
                return None

    if subject is not None and object is not None:
        if (subject, object) not in facts:
            return None
        edges = facts[(subject, object)]
        edges = _filter_by_predicate(edges)
        if edges is None:
            return None
        return {(subject, object): edges}

    else:
        new_facts = {}
        for (_source_node, _target_node), _edges in facts.items():
            if subject is not None and _source_node != subject:
                continue
            if object is not None and _target_node != object:
                continue
            _edges = _filter_by_predicate(_edges)
            if _edges is not None:
                new_facts[(_source_node, _target_node)] = _edges
        return new_facts