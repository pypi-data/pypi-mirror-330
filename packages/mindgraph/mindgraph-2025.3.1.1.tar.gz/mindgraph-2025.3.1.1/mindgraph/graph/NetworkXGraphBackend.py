import networkx as nx
from typing import List, Tuple, Dict, Optional, Callable, Union
from .GraphBackend import GraphBackend
from datetime import datetime
class NetworkXGraphBackend(GraphBackend):
    """
    NetworkX-based implementation of GraphBackend that supports multiple edges (relationships) between nodes.
    Uses a directed multigraph (MultiDiGraph), allowing multiple edges between the same node pairs.
    """

    def __init__(self):
        super().__init__()
        self.graph = nx.MultiDiGraph()

    def _copy(self) -> 'NetworkXGraphBackend':
        """
        Returns a copy of the graph.
        """
        new_graph_backend = NetworkXGraphBackend()
        new_graph_backend.graph = self.graph.copy()
        return new_graph_backend

    @property
    def _data_dict(self) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the data dictionary of the graph backend.
        Returns:
            Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]: a dictionary of the form:
            {
                (source_node, target_node): {
                    edge: metadata_dict
                    ...
                }
                ...
            }
        """
        result = {}
        for _source_node, _target_node, _edge, _metadata in self.graph.edges(data=True, keys=True):
            if (_source_node, _target_node) not in result:
                result[(_source_node, _target_node)] = {}
            edge_metadata = _metadata.copy()
            del edge_metadata['_edge']
            result[(_source_node, _target_node)][_edge] = edge_metadata

        return result

    def _has_node(self, node: str) -> bool:
        """
        Checks if a node exists in the graph.

        Args:
            node (str): The node to check.

        Returns:
            bool: True if the node exists, False otherwise.
        """
        return self.graph.has_node(node)

    def _add_node(self, node: str, metadata: Optional[Dict] = {}):
        """
        Adds a node to the graph if it does not already exist.

        Args:
            node (str): The node to add.
            **metadata: Additional metadata to store with the node.
        """
        self.graph.add_node(node, **metadata)

    def _add_edge(self, source_node: str, target_node: str, edge: str, metadata: Optional[Dict] = {}):
        """
        Adds an edge between two nodes with optional metadata.

        Args:
            source_node (str): The starting node of the edge.
            target_node (str): The ending node of the edge.
            edge (str): The label identifying the edge type.
            metadata_key (str): The key to store the metadata under.
            metadata (Dict): Additional metadata to store with the edge.

        Example:
            _add_edge("Alice", "Bob", "knows", confidence=0.9)

        NetworkX allows multiple edges between the same node pairs using the 'key' parameter.
        Metadata of the edge is stored in a dictionary
        """
        if not isinstance(edge, str):
            raise TypeError("Edge must be a string.")
        
        # unfortunately edge name is not stored in a way that is usable in in_edges and out_edges, therefore we should store it in metadata
        metadata = metadata.copy()
        metadata['_edge'] = edge
        
        if self.graph.has_edge(source_node, target_node, key=edge):
            # Ensure complete replacement of metadata
            self.graph[source_node][target_node][edge].clear()  # Remove old metadata
            self.graph[source_node][target_node][edge].update(metadata)  # Add new metadata

        else:
            self.graph.add_edge(u_for_edge=source_node, v_for_edge=target_node, key=edge, **metadata)

    def _out_edges(self, node: str) -> List[Tuple[str, str, Dict]]:
        """
        Retrieves all outgoing edges from a node.

        Args:
            node (str): The node to retrieve outgoing edges from.

        Returns:
            Dict[Tuple[str, str], Dict[str, Dict]]: A dictionary where keys are tuples of (source_node, target_node) and values are dictionaries of edges and their metadata.

        Example Output:
            {
                ("Alice", "Bob"): {"knows": metadata},
                ("Alice", "Charlie"): {"friend_of": metadata}
            }
        """

        result = {}
        for source_node, target_node, edge_dict in self.graph.out_edges(node, data=True):
            if (source_node, target_node) not in result:
                result[(source_node, target_node)] = {}
            edge_name = edge_dict['_edge']
            if edge_name not in result[(source_node, target_node)]:
                result[(source_node, target_node)][edge_name] = {}
            metadata = edge_dict.copy()
            del metadata['_edge']
            result[(source_node, target_node)][edge_name] = metadata

        return result


    def _in_edges(self, node: str) -> List[Tuple[str, str, Dict]]:
        """
        Retrieves all incoming edges to a node.

        Args:
            node (str): The node to retrieve incoming edges for.

        Returns:
            Dict[Tuple[str, str], Dict[str, Dict]]: A dictionary where keys are tuples of (source_node, target_node) and values are dictionaries of edges and their metadata.

        Example Output:
            {
                ("Bob", "Alice"): {"knows": metadata},
                ("Charlie", "Alice"): {"friend_of": metadata}
            }
        """
        result = {}
        for source_node, target_node, edge_dict in self.graph.in_edges(node, data=True):
            if (source_node, target_node) not in result:
                result[(source_node, target_node)] = {}
            edge_name = edge_dict['_edge']
            if edge_name not in result[(source_node, target_node)]:
                result[(source_node, target_node)][edge_name] = {}
            metadata = edge_dict.copy()
            del metadata['_edge']
            result[(source_node, target_node)][edge_name] = metadata

        return result

    def _has_edge(self, source_node: str, target_node: str, edge: Optional[str] = None) -> bool:
        """
        Checks if any edge exists between two nodes.

        Args:
            source_node (str): The starting node.
            target_node (str): The ending node.
            edge (Optional[str]): The specific edge label to check. If None, checks for any edge.

        Returns:
            bool: True if at least one edge exists between the nodes, False otherwise.
        """
        if edge is None:
            return self.graph.has_edge(source_node, target_node)
        else:
            return self.graph.has_edge(source_node, target_node, key=edge)

    def _remove_edge(self, source_node: str, target_node: str, edge: Optional[str] = None, raise_if_not_found: bool = False):
        """
        Removes an edge between two nodes. If no specific edge label is provided, all edges between
        the nodes are removed.

        Args:
            source_node (str): The starting node.
            target_node (str): The ending node.
            edge (Optional[str]): The specific edge label to remove. If None, all edges are removed.

        Example:
            _remove_edge("Alice", "Bob", "knows")  # Removes only the "knows" edge.
            _remove_edge("Alice", "Bob")  # Removes all edges between Alice and Bob.
        """
        if self.graph.has_edge(source_node, target_node):
            if edge:
                if self.graph.has_edge(source_node, target_node, key=edge):  # Prevent NetworkXError
                    self.graph.remove_edge(source_node, target_node, key=edge)
                elif raise_if_not_found:
                    raise KeyError(f"Edge {edge} not found between {source_node} and {target_node}")
            else:
                # Get a list of edge keys before removing to avoid KeyError
                edge_keys = list(self.graph[source_node][target_node].keys())
                if len(edge_keys) == 0:
                    raise RuntimeError(f"Edges are found between {source_node} and {target_node} but the result is an empty dictionary")
                for edge_key in edge_keys:
                    if self.graph.has_edge(source_node, target_node, key=edge_key):  # Prevent KeyError
                        self.graph.remove_edge(source_node, target_node, key=edge_key)
        elif raise_if_not_found:
            raise KeyError(f"No edge found between {source_node} and {target_node}")

    _delete_edge = _remove_edge

    def _remove_edges(
            self,
            source_node: Optional[str] = None,
            edge: Optional[str] = None,
            target_node: Optional[str] = None,
            raise_if_not_found: bool = False
        ):
        if source_node is not None and target_node is not None:
            return self._remove_edge(source_node=source_node, target_node=target_node, edge=edge, raise_if_not_found=raise_if_not_found)
        
        else:
            all_edges = self._get_edges(source_node=source_node, target_node=target_node, edge=edge)
            for (_source_node, _target_node), edges in all_edges.items():
                if source_node is not None and source_node != _source_node:
                    continue
                if target_node is not None and target_node != _target_node:
                    continue
                self._remove_edge(source_node=_source_node, target_node=_target_node, edge=edge, raise_if_not_found=raise_if_not_found)
            return
                

    def _remove_node(self, node: str):
        """
        Removes a node from the graph along with all its connected edges.

        Args:
            node (str): The node to remove.

        Example:
            _remove_node("Alice")  # Removes Alice and all edges connected to Alice.
        """
        if self.graph.has_node(node):
            self.graph.remove_node(node)
        else:
            raise KeyError(f"Node {node} not found in graph")
        
    @staticmethod
    def _remove_edge_name_from_metadata(edge_dict: Dict) -> Dict:
        edge_dict = edge_dict.copy()
        del edge_dict['_edge']
        return edge_dict
        
    def _get_edges(self, source_node: Optional[str] = None, target_node: Optional[str] = None, edge: Optional[str] = None) -> Dict[str, Dict]:
        """
        Retrieves metadata for all edges between two nodes.
        """
        if source_node is None and target_node is None:
            # get all edges
            all_edges = self.graph.edges(data=True, keys=True)

            result = {}
            for source_node, target_node, _edge, edge_dict in all_edges:
                if edge is None or _edge == edge:
                    if (source_node, target_node) not in result:
                        result[(source_node, target_node)] = {}
                    result[(source_node, target_node)][_edge] = self._remove_edge_name_from_metadata(edge_dict)

            return result

        if source_node is None or target_node is None:
            if source_node is None:
                all_edges = self._in_edges(node=target_node)
            else:
                all_edges = self._out_edges(node=source_node)
            if edge is None:
                return all_edges
            else:
                return {
                    (source_node, target_node): {edge: all_edges_dict[edge]}
                    for (source_node, target_node), all_edges_dict in all_edges.items()
                    if edge in all_edges_dict
                }

        if edge is None:
            return {
                (source_node, target_node): {
                    edge: self._remove_edge_name_from_metadata(edge_dict)
                    for edge, edge_dict in self._get_edge_data(source_node=source_node, target_node=target_node).items()
                }
            }
        else:
            single_edge = self._get_edge_data(source_node=source_node, target_node=target_node, edge=edge)
            edge_dict = self._remove_edge_name_from_metadata(single_edge)

            return {
                (source_node, target_node): {edge: edge_dict}
            }

    def _get_edge_data(self, source_node: str, target_node: str, edge: Optional[str] = None) -> Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]:
        """
        Retrieves metadata for a specific edge between two nodes.
        """
        return self.graph.get_edge_data(source_node, target_node, key=edge) or {}

    def _clear_graph(self):
        """
        Removes all nodes and edges from the graph.

        Example:
            _clear_graph()  # Completely resets the graph.
        """
        self.graph.clear()

    def _n_edges(self) -> int:
        """
        Returns the number of edges in the graph.
        """
        return self.graph.number_of_edges()
