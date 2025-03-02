from . import GraphBackend, NetworkXGraphBackend, SimpleGraphBackend
from typing import Union, Optional, Dict, List, Tuple, Literal, Generator, Set
from datetime import datetime
from collections import deque
from .operations_on_facts import convert_facts_to_dataframe, convert_facts_to_list_of_dictionaries, filter_facts
from .operations_on_facts import convert_facts_to_abstract_graph_dict, convert_facts_to_abstract_graph
from .operations_on_facts import validate_facts_format
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from ..hybrid_fact_db import Fact

class GraphBackendInterface:
    """
    This class ensures what goes into the graph backend and comes out of the graph backend is valid

    The graph backend should support: multiple edges between the same node pairs
    It should also support multiple facts per edge

    """

    DEFAULT_EDGE_DEPTH_EXCEPTIONS = {'is_subject_of': 0, 'is_object_of': 0}
    DEFAULT_SOURCE_NODE_DEPTH_EXCEPTIONS = {'fact': 0}
    FACTS_DICTIONARY_FORMAT_EXAMPLE = {
        ('sournce_node/subject', 'target_node/object'): {
            'edge/predicate': {
                'fact_id': {'fact_source': 'Fact Source', 'timestamp': 'Timestamp', 'metadata': {}}
            }
        },
        ('Berlin', 'Germany'): {
            'capital_of': {
                'fact_1': {'fact_source': 'Wikipedia', 'timestamp': datetime.now(), 'metadata': {}},
                'fact_2': {'fact_source': 'Google', 'timestamp': datetime.now(), 'metadata': {}}
            },
            'city_in': {
                'fact_3': {'fact_source': 'Google', 'timestamp': datetime.now(), 'metadata': {}}
            }
        },
        ('Germany', 'Europe'): {
            'country_in': {
                'fact_4': {'fact_source': 'Google', 'timestamp': datetime.now(), 'metadata': {}}
            }
        }
    }

    def __init__(
            self, graph_backend: Union[NetworkXGraphBackend, SimpleGraphBackend, GraphBackend], 
            edge_depth_exceptions: Optional[Dict[str, int]] = None,
            case_sensitive: bool = False
        ):
        """
        Args:
            graph_backend (Union[NetworkXGraphBackend, SimpleGraphBackend, GraphBackend]): The graph backend to use.
            edge_depth_exceptions (Optional[Dict[str, int]]): A dictionary of depth exceptions for the graph backend based on edge value
        """
        self.graph_backend = graph_backend
        self.edge_depth_exceptions = edge_depth_exceptions or {}
        self.case_sensitive = case_sensitive
        self.delete_facts = self.remove_facts

    # GENERAL HELPER METHODS

    def _fix_case(self, string: str) -> str:
        """
        Fixes the case of a string.
        """
        if string is None:
            return None
        return string.lower() if not self.case_sensitive else string

    # PROPERTIES

    @property
    def data_dict(self) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the data dictionary of the graph backend.
        """
        return self.graph_backend.data_dict

    # HAS METHODS

    def _has_edge(self, source_node: str, edge: str, target_node: str) -> bool:
        """
        Checks if an edge exists between two nodes.
        """
        source_node = self._fix_case(source_node)
        edge = self._fix_case(edge)
        target_node = self._fix_case(target_node)
        return self.graph_backend.has_edge(source_node=source_node, edge=edge, target_node=target_node)
    
    def _has_node(self, node: str) -> bool:
        """
        Checks if a node exists in the graph backend.
        """
        node = self._fix_case(node)
        return self.graph_backend.has_node(node=node)
    
    # HELPER GET METHODS

    def _get_depth(self, edge: str, metadata: Optional[Dict] = None) -> int:
        """
        Gets the depth of an edge.
        """
        if metadata is not None and 'edge_depth' in metadata:
            return metadata['edge_depth']
        return self.edge_depth_exceptions.get(edge, 1)
    
    def get_number_of_connected_pairs(self) -> int:
        """
        Gets the number of connected subject-object pairs in the graph backend.
        """
        return len(self.data_dict)
    
    def get_number_of_edges(self) -> int:
        """
        Gets the number of edges in the graph backend.
        """
        number_of_edges_per_connected_pair = [len(_edges_dict) for (_source_node, _target_node), _edges_dict in self.data_dict.items()]
        return sum(number_of_edges_per_connected_pair)
    
    get_number_of_facts = get_number_of_edges

    def get_number_of_fact_sources(self) -> int:
        """
        Gets the number of fact sources in the graph backend.
        """
        number_of_fact_sources_per_connected_pairs = [
            len(_facts_as_dict) 
            for (_source_node, _target_node), _edges_dict in self.data_dict.items() 
            for _edge, _facts_as_dict in _edges_dict.items()
        ]
        return sum(number_of_fact_sources_per_connected_pairs)

    # MAIN GET METHODS

    def _get_edges(
            self, 
            source_node: Optional[str] = None, 
            edge: Optional[str] = None, 
            target_node: Optional[str] = None
        ) -> Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]:
        """
        Gets all edges between two nodes.
        Args:
            source_node (Optional[str]): The source node.
            edge (Optional[str]): The edge.
            target_node (Optional[str]): The target node.
        Returns:
            Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]: A dictionary of edges between the two nodes.

        Example output:
        {
            (source_node_1, target_node_1): {
                edge_1: {
                    fact_1: {...},
                    fact_2: {...},
                    ...
                },
                edge_2: {
                    fact_3: {...},
                    fact_4: {...},
                    ...
                },
                ...
            },
            (source_node_2, target_node_2): {
                edge_1: {
                    fact_1: {...},
                    fact_2: {...},
                    ...
                },
                ...
            },
            ...
        }
        """
        source_node = self._fix_case(source_node)
        edge = self._fix_case(edge)
        target_node = self._fix_case(target_node)
        return self.graph_backend.get_edges(source_node=source_node, edge=edge, target_node=target_node) or {}
    
    def _get_edge_if_exists(
            self, source_node: str, edge: str, target_node: str, default: any = {}
        ) -> Optional[Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets an edge between two nodes with optional metadata.
        Instead of returning:
        {
            (source_node_1, target_node_1): {
                edge_1: {
                    fact_1: {...},
                    fact_2: {...},
                    ...
                },
            }
        }

        It returns:
        facts_1: {...},
        facts_2: {...},
        ...
        """
        if not isinstance(source_node, str):
            raise TypeError(f"Source node is not a string: {source_node}")
        if not isinstance(edge, str):
            raise TypeError(f"Edge is not a string: {edge}")
        if not isinstance(target_node, str):
            raise TypeError(f"Target node is not a string: {target_node}")

        source_node = self._fix_case(source_node)
        edge = self._fix_case(edge)
        target_node = self._fix_case(target_node)
        if self._has_edge(source_node=source_node, edge=edge, target_node=target_node):
            source_target_to_edges = self._get_edges(source_node=source_node, edge=edge, target_node=target_node)
            edges_between_source_and_target = source_target_to_edges[(source_node, target_node)]
            facts_for_this_edge = edges_between_source_and_target[edge]
            return facts_for_this_edge
        return default
    
    def _get_outgoing_edges(self, node: str) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the outgoing edges of a node.
        Args:
            node (str): The node to get the outgoing edges of.
        Returns:
            Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]: A dictionary of outgoing edges.
        output is in the form of:
        {
            (node, target_node): {
                edge1: {
                    fact_1: {...},
                    fact_2: {...}
                },
                ...
            },
            ...
        }
        """
        node = self._fix_case(node)
        return self.graph_backend._out_edges(node=node)

    # COMPLEX GET METHODS

    def _get_incoming_edges(self, node: str) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the incoming edges of a node.
        Args:
            node (str): The node to get the incoming edges of.
        Returns:
            Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]: A dictionary of incoming edges.
        """
        node = self._fix_case(node)
        return self.graph_backend._in_edges(node=node)
        
    def _get_neighbours(
            self, nodes: Union[str, Tuple, List[str]], depth: int = 1, direction: str = "both", 
            edges: Optional[Union[str, Tuple, List[str]]] = None,
            fields: Optional[Union[str, Tuple[str, ...]]] = ('fact_id', 'fact_source', 'timestamp', 'depth'), # fact sources: ('fact_id', 'fact_source', 'timestamp')
            fact_sources: Optional[Union[str, Tuple, List[str]]] = None,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            metadata_type: Literal['tuple', 'dict'] = 'dict',
            _visited: Optional[Set[str]] = None,
            _queue: Optional[deque] = None,
            output_type: Literal['dict', 'list', 'dataframe'] = 'list'
        ) -> Dict[Tuple[str, str], Dict[str, Union[Tuple, Dict]]]:

        """
        Gets the neighbours_dict of a node.
        Args:
            node (Union[str, Tuple, List[str]]): The nodes to get the neighbours_dict of. 
            depth (int): The depth of the neighbours_dict to get.
            direction (str): The direction of the neighbours_dict to get.
            edge (Optional[str]): If specified, only the neighbours_dict with this edge will be returned. It is the same as predicate
            tuple_format (Optional[Union[str, Tuple[str, ...]]]): The format of the neighbours_dict to get.
            return_as_dictionaries (bool): Whether to return the neighbours_dict as dictionaries or tuples.
            fact_id_starts_with (str): The prefix of the fact ids.
            fact_source (Optional[str]): If specified, only the neighbours_dict with this fact source will be returned.
            start_time (Optional[datetime]): If specified, only the neighbours_dict with this start time will be returned.
            end_time (Optional[datetime]): If specified, only the neighbours_dict with this end time will be returned.
        Returns:
            Dict[Tuple[str, str], Dict[str, Union[Tuple, Dict]]]: A dictionary of neighbours_dict.
        Example outputs:
        # as a list of tuples
        [
            (source_node, edge, target_node, fact_sources),
            ...
        ]

        # as a list of dictionaries
        [ 
            {'source_node': source_node, 'edge': edge, 'target_node': target_node, 'fact_sources': fact_sources},
            ...
        ]

        # as a dictionary of lists of tuples
        {
            'node1': [(node1, node2): 
            ...
        }
        """

        acceptable_fields = {'source_node', 'edge', 'target_node', 'fact_source', 'timestamp', 'depth', 'fact_id'}
        incorrect_fields = set(fields) - acceptable_fields
        if incorrect_fields:
            raise ValueError(f"The fields {incorrect_fields} are not valid. They must be one of {acceptable_fields}.")

        if metadata_type == 'tuple':
            def _format_metadata(**kwargs):
                return tuple(kwargs[field] for field in fields)
        elif metadata_type == 'dict':
            def _format_metadata(**kwargs):
                return {field: kwargs[field] for field in fields}
        else:
            raise ValueError(f"Metadata type {metadata_type} is not valid. It must be 'tuple' or 'dict'.")
        
        if isinstance(nodes, str):
            nodes = [nodes]

        missing_nodes = [_node for _node in nodes if not self._has_node(_node)]
        if missing_nodes:
            raise ValueError(f"Nodes {missing_nodes} do not exist in the graph.")

        if isinstance(edges, str):
            edges = [edges]
        if isinstance(fact_sources, str):
            fact_sources = [fact_sources]
        edges = set(edges) if edges else None
        fact_sources = set(fact_sources) if fact_sources else None

        missing_nodes = [ _node for _node in nodes if not self._has_node(_node)]
        if missing_nodes:
            raise ValueError(f"The nodes {missing_nodes} do not exist in the graph backend.")

        # add the nodes to the queue
        queue = _queue or deque()
        visited = _visited or set()
        for _node in nodes:
            if _node not in visited:
                queue.append((_node, 0))
                visited.add(_node)

        if output_type == 'dict':
            neighbours_dict = {}
            neighbours_list = None
        else:
            neighbours_list = []
            neighbours_dict = None
        
        while queue:
            current_node, _current_depth = queue.popleft()
            if _current_depth >= depth:
                continue

            all_edges = {}
            if direction in ["outgoing", "both"]:
                all_edges["outgoing"] = self._get_outgoing_edges(node=current_node)
            if direction in ["incoming", "both"]:
                all_edges["incoming"] = self._get_incoming_edges(node=current_node)

            for _direction, _direction_dict in all_edges.items():
                for (_source_node, _target_node), _edges in _direction_dict.items():
                    if edges is None:
                        relevant_edges = {e: _facts for e, _facts in _edges.items()}
                    else:
                        relevant_edges = {e: _facts for e, _facts in _edges.items() if e in edges}

                    neighbour_node = _target_node if _direction == 'outgoing' else _source_node

                    source_target_key = (_source_node, _target_node)
                    if output_type == 'dict' and source_target_key not in neighbours_dict:
                        neighbours_dict[source_target_key] = {}
                    
                    for _edge, _facts_as_dict in relevant_edges.items():
                        edge_depth = self._get_depth(edge=_edge, metadata=_facts_as_dict)
                        next_depth = _current_depth + edge_depth
                        if next_depth > depth:
                            continue

                        if output_type == 'dict':
                            neighbours_dict[source_target_key].setdefault(_edge, {})

                        for _fact_id, _metadata in _facts_as_dict.items():
                            if 'fact_source' not in _metadata: # <- ToDo: remove this, it is a temporary check
                                print('*'*100, '\n', 'facts_as_dict', _facts_as_dict, '\n', '*'*100, '\n')
                                raise ValueError(f"Edge {_edge}, Fact_id: `{_fact_id}` has no fact source. It is {_metadata}, {_facts_as_dict}")
                            fact_source = _metadata['fact_source']
                            timestamp = _metadata['timestamp']
                            if fact_sources is not None and fact_source not in fact_sources:
                                continue
                            if start_time is not None and timestamp < start_time:
                                continue
                            if end_time is not None and timestamp > end_time:
                                continue

                            if output_type == 'dict' and _fact_id not in neighbours_dict[source_target_key][_edge]:
                                # format the output
                                tuple_or_dict = _format_metadata(
                                    source_node=_source_node,
                                    edge=_edge,
                                    target_node=_target_node,
                                    fact_id=_fact_id,
                                    fact_source=fact_source,
                                    timestamp=timestamp,
                                    depth=next_depth
                                )
                                
                                neighbours_dict[source_target_key][_edge][_fact_id] = tuple_or_dict

                            if output_type != 'dict':
                                tuple_or_dict = _format_metadata(
                                    source_node=_source_node,
                                    edge=_edge,
                                    target_node=_target_node,
                                    fact_id=_fact_id,
                                    fact_source=fact_source,
                                    timestamp=timestamp,
                                    depth=next_depth
                                )
                                assert isinstance(tuple_or_dict, tuple) or isinstance(tuple_or_dict, dict)
                                neighbours_list.append(tuple_or_dict)

                        # End of [for fact_id, metadata in facts_as_dict.items()]
                        # if no facts are added to the edge, remove the empty dictionary
                        if output_type == 'dict' and not neighbours_dict[source_target_key][_edge]:
                            del neighbours_dict[source_target_key][_edge]

                        if neighbour_node not in visited:
                            visited.add(neighbour_node)
                            queue.append((neighbour_node, next_depth))

                    # End of [for edge, facts_as_dict in edges.items()]
                    # if no edges are added to the source_target_key, remove the empty dictionary
                    if output_type == 'dict' and not neighbours_dict[source_target_key]:
                        del neighbours_dict[source_target_key]
                    # end of for edge, facts_as_dict in edges.items()
                # end of for (source_node, target_node), edges in _direction_dict.items()
            # end of for _direction, _direction_dict in all_edges.items()

        if output_type == 'dict':
            return neighbours_dict
        elif output_type == 'list':
            return neighbours_list
        elif output_type == 'dataframe':
            return pd.DataFrame(data=neighbours_list, columns=fields).drop_duplicates()
        else:
            return neighbours_list


    def _get_neighbours_parallel(
            self, nodes: Union[str, Tuple, List[str]], depth: int = 1, direction: str = "both", 
            edges: Optional[Union[str, Tuple, List[str]]] = None,
            fields: Optional[Union[str, Tuple[str, ...]]] = ('fact_id', 'fact_source', 'timestamp', 'depth'), # fact sources: ('fact_id', 'fact_source', 'timestamp')
            fact_sources: Optional[Union[str, Tuple, List[str]]] = None,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            metadata_type: Literal['tuple', 'dictionary'] = 'dictionary',
            max_workers: Optional[int] = 4
        ) -> Dict[Tuple[str, str], Dict[str, Union[Tuple, Dict]]]:

        """
        Gets the neighbours_dict of a node in parallel.
        """

        if isinstance(nodes, str):
            nodes = [nodes]

        _visited = set()
        _queue = deque()
        visited_lock = threading.Lock()
        queue_lock = threading.Lock()

        def _process_nodes(node_batch: List[str]):
            with visited_lock:
                new_nodes = [node for node in node_batch if node not in _visited]
                _visited.update(new_nodes)

            if not new_nodes:
                return {}

            return self._get_neighbours(
                nodes=new_nodes,
                depth=depth,
                direction=direction,
                edges=edges,
                fields=fields,
                fact_sources=fact_sources,
                start_time=start_time,
                end_time=end_time,
                metadata_type=metadata_type,
                _visited=_visited,
                _queue=_queue
            )

        node_batches = [nodes[i::max_workers] for i in range(max_workers)]
        result = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_process_nodes, batch): batch for batch in node_batches}
            for future in as_completed(futures):
                result.append(future.result())

        # Merge results from all batches
        merged_result = {}
        for res in result:
            pass # TODO: complete this

            

    def get_facts_about(
            self, 
            entities: Optional[Union[str, Tuple, List[str]]] = None,
            direction: Optional[Literal['incoming', 'outgoing', 'both']] = 'both',
            depth: int = 1,
            predicates: Optional[Union[str, Tuple, List[str]]] = None,
            fact_sources: Optional[Union[str, Tuple, List[str]]] = None,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            fields: Optional[Union[str, Tuple[str, ...]]] = ('source_node', 'edge', 'target_node', 'fact_id', 'fact_source', 'timestamp', 'depth'),
            metadata_type: Literal['tuple', 'dict'] = 'dict',
            verify_output_format: bool = False,
            return_abstract_graph: bool = False,
            output_type: Literal['dict', 'list', 'dataframe'] = 'list'
        ) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[Dict, Tuple]]]]:
        #         ^(subject, obj), ^{edge:  ^{fact_id: ^{fact_source: ..., timestamp: ..., metadata: ...}}} 
        #  Or     ^(subject, obj), ^{edge:  ^{fact_id: (fact_source, timestamp, ...)}} 
        """
        Gets the facts about a subject or object.
        Args:
            entities (Optional[Union[str, Tuple, List[str]]]): The entities to get the facts about.
            direction (Optional[Literal['incoming', 'outgoing', 'both']]): The direction of the facts to get.
            depth (int): The depth of the facts to get.
            predicates (Optional[Union[str, Tuple, List[str]]]): If specified, only the facts with these predicates will be returned.
            fact_sources (Optional[Union[str, Tuple, List[str]]]): If specified, only the facts with these fact sources will be returned.
            start_time (Optional[datetime]): If specified, only the facts with this start time will be returned.
            fields (Optional[Union[str, Tuple[str, ...]]]): The fields to return.
            metadata_type (Literal['tuple', 'dictionary']): The type of the return value.
        """
        if not isinstance(direction, str):
            raise TypeError(f"Direction is not a string. It is a {type(direction)}: {direction}")
        if direction not in ['incoming', 'outgoing', 'both']:
            raise ValueError(f"Direction is not valid. It must be one of ['incoming', 'outgoing', 'both']. It is {direction}")

        results = self._get_neighbours(
            nodes=entities,
            depth=depth,
            direction=direction,
            edges=predicates,
            metadata_type=metadata_type,
            fact_sources=fact_sources,
            start_time=start_time,
            end_time=end_time,
            fields=fields,
            output_type=output_type
        )

        if verify_output_format:
            if not isinstance(results, dict):
                raise TypeError(f"Results are not a dictionary. They are a {type(results)}: {results}")
            for key, value in results.items():
                if not isinstance(key, tuple):
                    raise TypeError(f"Results are not a dictionary of tuples. They are a dictionary of {type(key)}: {key}")
                if len(key) != 2:
                    raise TypeError(f"Results are not a dictionary of tuples with two elements. They are a dictionary of tuples with {len(key)} elements: {key}")
                if not isinstance(value, dict):
                    raise TypeError(f"Results are not a dictionary of dictionaries. They are a dictionary of {type(value)}: {value}")
                for edge, facts_as_dict in value.items():
                    if not isinstance(edge, str):
                        raise TypeError(f"Results are not a dictionary of edge dictionaries with string (edge) keys. They are a dictionary of edge dictionaries with {type(edge)} edge keys: {edge}")
                    if not isinstance(facts_as_dict, dict):
                        raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. They are a dictionary of edge dictionaries with {type(facts_as_dict)} fact dictionaries: {facts_as_dict}")
                    for fact_id, metadata in facts_as_dict.items():
                        if not isinstance(fact_id, str):
                            raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. The fact ids are not strings. They are {type(fact_id)}: {fact_id}")
                        if not fact_id.startswith('fact_'):
                            raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. The fact ids are not strings that start with 'fact_'. They are {fact_id}")
                        if metadata_type == 'tuple':
                            if not isinstance(metadata, tuple):
                                raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. The metadata is not a tuple. It is a {type(metadata)}: {metadata}")
                        elif metadata_type == 'dictionary':
                            if not isinstance(metadata, dict):
                                raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. The metadata is not a dictionary. It is a {type(metadata)}: {metadata}")
                        if len(metadata) != len(fields):
                            raise TypeError(f"Results are not a dictionary of edge dictionaries with fact dictionaries as values. The metadata is not a dictionary with the same length as the fields. It is a dictionary with {len(metadata)} elements: {metadata}")
        
        if return_abstract_graph:
            return self.convert_facts_to_abstract_graph(results)
        return results

    @staticmethod
    def _convert_facts_to_generator(
        facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[Dict, Tuple]]]]
    ) -> Generator[Dict[str, Union[str, int, float, bool, datetime]], None, None]:
        """
        Converts a dictionary of facts to a generator of dictionaries.
        """
        for (subject, object), edges in facts.items():
            for edge, facts_as_dict in edges.items():
                for fact_id, metadata in facts_as_dict.items():
                    yield {
                        'subject': subject,
                        'object': object,
                        'edge': edge,
                        'fact_id': fact_id,
                        'fact_source': metadata['fact_source'],
                        'timestamp': metadata['timestamp'],
                        'metadata': metadata['metadata']
                    }

    @staticmethod
    def _convert_facts_to_list_of_dictionaries(
        facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[Dict, Tuple]]]]
    ) -> List[Dict[str, Union[str, int, float, bool, datetime]]]:
        """
        Converts a dictionary of facts to a list of dictionaries.
        """
        return list(self._convert_facts_to_generator(facts=facts))

    @staticmethod
    def _convert_facts_to_fact_objects(
        facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[Dict, Tuple]]]]
    ) -> List['Fact']:
        """
        Converts a dictionary of facts to a list of Fact objects.
        """
        result = []
        for dictionary in self._convert_facts_to_generator(facts=facts):
            # edge is predicate
            dictionary['predicate'] = dictionary['edge']
            del dictionary['edge']
            result.append(Fact.from_dictionary(dictionary=dictionary))
        return result

    # ADD METHODS

    def _add_edge(self, source_node: str, edge: str, target_node: str, facts_dict: Optional[Dict] = {}):
        """
        Adds an edge between two nodes with optional metadata.
        """
        source_node = self._fix_case(source_node)
        edge = self._fix_case(edge)
        target_node = self._fix_case(target_node)
        self.graph_backend.add_edge(
            source_node=source_node,
            edge=edge,
            target_node=target_node,
            metadata=facts_dict
        )
    
    def add_fact(
            self, fact_id: str, subject: str, predicate: str, object: str, 
            fact_source: str, timestamp: Optional[datetime] = None, metadata: Optional[Dict] = {},
            edge_depth: Optional[int] = None
        ):
        """
        Adds a fact to the graph backend.
        Args:
            fact_id (str): The id of the fact.
            subject (str): The subject of the fact.
            predicate (str): The predicate of the fact.
            object (str): The object of the fact.
            fact_source (str): The source of the fact.
            timestamp (Optional[datetime]): The timestamp of the fact.
        edges = {
            predicate_1: {
                fact_1: {...},
                fact_2: {...}
            },
            predicate_2: {
                fact_3: {...},
                fact_4: {...}
            }
        }
        """
        _object = object
        del object

        # if the edge exists, add the fact to the edge
        edge = self._get_edge_if_exists(source_node=subject, edge=predicate, target_node=_object, default={})
        edge[fact_id] = {
            'fact_source': fact_source,
            'timestamp': timestamp,
            'metadata': metadata
        }

        if edge_depth is not None:
            if 'edge_depth' not in edge:
                edge['edge_depth'] = edge_depth
            elif 'edge_depth' in edge and edge['edge_depth'] != edge_depth:
                raise ValueError(f"Edge depth cannot be overwritten. It is {edge['edge_depth']} and you are trying to set it to {edge_depth}")

        self._add_edge(
            source_node=subject,
            edge=predicate,
            target_node=_object,
            facts_dict=edge
        )
    
    # REMOVE METHODS
    
    def _remove_node(self, node: str):
        """
        Removes a node from the graph backend.
        """
        if self._has_node(node):
            self.graph_backend.remove_node(node=node)
        else:
            raise KeyError(f"Node {node} not found in graph backend")
        
    def _remove_edge(self, source_node: str, edge: str, target_node: str):
        self.graph_backend.remove_edge(source_node=source_node, edge=edge, target_node=target_node)
        # graph_backend automatically removes the connection pair if there are no edges left

    def _remove_edges(self, source_node: Optional[str] = None, edge: Optional[str] = None, target_node: Optional[str] = None):
        # removes edges with the given criteria
        self.graph_backend.remove_edges(
            source_node=source_node,
            edge=edge,
            target_node=target_node
        )

    def remove_fact(self, fact_id: str, subject: str, predicate: str, object: str):
        """
        Removes a fact from the graph backend.
        """
        _object = object
        del object

        facts_as_dict = self._get_edge_if_exists(source_node=subject, edge=predicate, target_node=_object, default={})
        if fact_id in facts_as_dict:
            del facts_as_dict[fact_id]
        else:
            raise KeyError(f"Fact {fact_id} not found in edge {subject} - {predicate} - {_object}")
        
        if len(facts_as_dict) == 0 or len(facts_as_dict) == 1 and 'edge_depth' in facts_as_dict:
            self._remove_edges(source_node=subject, edge=predicate, target_node=_object)
        else:
            self._add_edge(
                source_node=subject,
                edge=predicate,
                target_node=_object,
                facts_dict=facts_as_dict
            )

    def remove_facts(
            self, subject: Optional[str] = None, predicate: Optional[str] = None, object: Optional[str] = None, fact_id: Optional[str] = None,
            raise_if_fact_id_not_found: bool = True
        ):
        """
        Removes facts from the graph backend.
        the arguments are optional and narrow down the scope of the deletion
        """
        _object = object
        del object
        subject = self._fix_case(subject)
        predicate = self._fix_case(predicate)
        _object = self._fix_case(_object)

        if fact_id is None:
            self._remove_edges(
                source_node=subject,
                edge=predicate,
                target_node=_object
            )
        else:
            nodes_to_edges_dict = self._get_edges(
                source_node=subject,
                edge=predicate,
                target_node=_object
            )
            for (source_node, target_node), edges in nodes_to_edges_dict.items():
                for edge, facts_as_dict in edges.items():
                    if fact_id in facts_as_dict:
                        self.remove_fact(fact_id=fact_id, subject=source_node, predicate=edge, object=target_node)
                        return
            if raise_if_fact_id_not_found:
                raise KeyError(f"Fact {fact_id} not found in edge with subject:{subject} - predicate:{predicate} - object:{_object}")
            
    # STATIC VALIDATION METHODS

    @staticmethod
    def _validate_facts_format(
        dictionary: Dict[Tuple[str, str], Dict[str, Dict]],
        fact_id_starts_with: str = 'fact_',
        metadata_type: Literal['tuple', 'dictionary', 'either'] = 'either'
    ):
        """
        Validates the format of a dictionary of facts.
        Args:
            dictionary (Dict[Tuple[str, str], Dict[str, Dict]]): The dictionary of facts to validate.
            fact_id_starts_with (str): The prefix of the fact id.
            metadata_type: The type of metadata to validate.
        Returns:
            bool: True if the format is valid, False otherwise.
        """
        return validate_facts_format(dictionary=dictionary, fact_id_starts_with=fact_id_starts_with, metadata_type=metadata_type)
                     
    @staticmethod
    def _verify_outgoing_edges(node: str, outgoing_edges: Dict[Tuple[str, str], Dict[str, Dict]], fact_id_starts_with: str = 'fact_'):
        for (source_node, target_node), edges in outgoing_edges.items():
            # check the source_node is the node
            if source_node != node:
                raise ValueError(f"Source node {source_node} is not the node {node}")
            
            # check the edges are a dictionary
            if not isinstance(edges, dict):
                raise TypeError(f"Edges are not a dictionary for node {node} but a {type(edges)}: {edges}")
            
            # check the edges are a dictionary of strings to dictionaries
            for edge, facts_as_dict in edges.items():
                if not isinstance(edge, str):
                    raise TypeError(f"Edge is not a string for node {node}")
                if not isinstance(facts_as_dict, dict):
                    raise TypeError(f"Metadata is not a dictionary for node {node} and edge {edge}: {facts_as_dict}")
                
                # fact_ids are the keys of the metadata
                for fact_id, metadata in facts_as_dict.items():
                    if not fact_id.startswith(fact_id_starts_with):
                        raise KeyError(f"Fact id {fact_id} does not start with {fact_id_starts_with} for node {node} and edge {edge} with metadata: {metadata}")
                    
        return True

    @staticmethod
    def _verify_incoming_edges(node: str, incoming_edges: Dict[Tuple[str, str], Dict[str, Dict]], fact_id_starts_with: str = 'fact_'):
        for (source_node, target_node), edges in incoming_edges.items():
            # check the target_node is the node
            if target_node != node:
                raise ValueError(f"Target node {target_node} is not the node {node}")
            
            # check the edges are a dictionary
            if not isinstance(edges, dict):
                raise TypeError(f"Edges are not a dictionary for node {node} but a {type(edges)}: {edges}")

            # check the edges are a dictionary of strings to dictionaries
            for edge, facts_as_dict in edges.items():
                if not isinstance(edge, str):
                    raise TypeError(f"Edge is not a string for node {node}")
                if not isinstance(facts_as_dict, dict):
                    raise TypeError(f"Metadata is not a dictionary for node {node} and edge {edge}: {facts_as_dict}")

                # fact_ids are the keys of the metadata
                for fact_id, metadata in facts_as_dict.items():
                    if not fact_id.startswith(fact_id_starts_with):
                        raise KeyError(f"Fact id {fact_id} does not start with {fact_id_starts_with} for node {node} and edge {edge} with metadata: {metadata}")
                    
        return True

    # STATIC CONVERSION METHODS

    @staticmethod
    def convert_facts_to_dataframe(
        facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]
    ) -> pd.DataFrame:
        """
        Converts a dictionary of facts to a pandas DataFrame.
        Args:
            facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
            direction (Optional[Literal['LR', 'RL', 'TB', 'BT']]): The direction of the facts.
        Returns:
            pd.DataFrame: A pandas DataFrame containing the facts.
        """
        return convert_facts_to_dataframe(facts=facts)

    @staticmethod
    def convert_facts_to_list_of_dictionaries(
        facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]],
    ) -> List[Dict[str, Union[str, int, float, bool, datetime]]]:
        """
        Converts a dictionary of facts to a list of dictionaries.
        Args:
            facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
        Returns:
            List[Dict[str, Union[str, int, float, bool, datetime]]]: A list of dictionaries containing the facts.
        """
        return convert_facts_to_list_of_dictionaries(facts=facts)

    @staticmethod
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
        return convert_facts_to_abstract_graph_dict(facts=facts, direction=direction)

    @staticmethod
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
        return convert_facts_to_abstract_graph(facts=facts, direction=direction, **kwargs)

    # STATIC HELPER METHODS

    @staticmethod
    def count(facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]], key: Literal['pairs', 'edges', 'facts']) -> int:
        """
        Counts the number of pairs, edges, or facts in the facts dictionary.
        """
        
        if isinstance(facts, pd.DataFrame):
            if key == 'pairs':
                return facts[['source_node', 'target_node']].drop_duplicates().shape[0]
            elif key == 'edges':
                return facts[['source_node', 'target_node', 'edge']].drop_duplicates().shape[0]
            elif key == 'facts':
                return facts[['source_node', 'target_node', 'edge', 'fact_id']].drop_duplicates().shape[0]
            else:
                raise ValueError(f"Invalid key: {key}")

        if len(facts) == 0:
            return 0
        metadata_type = 'tuple' if isinstance(facts[0], tuple) else 'dictionary'
        if isinstance(facts, dict):
            if key == 'pairs':
                return len(facts)
            elif key == 'edges':
                return sum(len(edges) for pair, edges in facts.items())
            elif key == 'facts':
                return sum(len(facts) for pair, edges in facts.items() for facts in edges.values())
            else:
                raise ValueError(f"Invalid key: {key}")
        elif isinstance(facts, list):
            if metadata_type == 'dictionary':
                if key == 'pairs':
                    return len(set((fact['source_node'], fact['target_node']) for fact in facts))
                elif key == 'edges':
                    return len(set((fact['source_node'], fact['target_node'], fact['edge']) for fact in facts))
                elif key == 'facts':
                    return len(set((fact['source_node'], fact['target_node'], fact['edge'], fact['fact_id']) for fact in facts))
                else:
                    raise ValueError(f"Invalid key: {key}")
            else:
                if key == 'pairs':
                    return len(set((fact[0], fact[1]) for fact in facts))
                elif key == 'edges':
                    return len(set((fact[0], fact[1], fact[2]) for fact in facts))
                elif key == 'facts':
                    return len(set((fact[0], fact[1], fact[2], fact[3]) for fact in facts))
                else:
                    raise ValueError(f"Invalid key: {key}")
        else:
            raise ValueError(f"Invalid facts: {facts}")

    @staticmethod
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
        _object = object
        del object

        return filter_facts(
            facts=facts, subject=subject, predicate=predicate, object=_object, 
            fact_id=fact_id, fact_source=fact_source, start_time=start_time, end_time=end_time, fields=fields
        )
