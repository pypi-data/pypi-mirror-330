from typing import List, Tuple, Dict, Optional, Union
from .GraphBackend import GraphBackend
from datetime import datetime

class SimpleGraphBackend(GraphBackend):
    """
    A simple in-memory graph backend using dictionaries for node and edge storage.
    Supports multiple edges between the same pair of nodes with O(1) lookups.
    """

    def __init__(self):
        super().__init__()
        self._nodes: Dict[str, Dict] = {}  # Stores node properties (if any)
        self._edges: Dict[Tuple[str, str], Dict[str, Dict]] = {}  # Stores edges as {(source, target): {edge: metadata}}

    @property
    def _data_dict(self) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the data dictionary of the graph backend.
        """
        return self._edges

    def _has_node(self, node: str) -> bool:
        """
        Checks if a node exists in the graph.

        Args:
            node (str): The node to check.

        Returns:
            bool: True if the node exists, False otherwise.
        """
        return node in self._nodes

    def _add_node(self, node: str, metadata: Optional[Dict] = {}):
        """
        Adds a node to the graph if it does not already exist.

        Args:
            node (str): The node to add.
            **metadata: Additional metadata to store with the node.
        """
        self._nodes[node] = metadata

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
        """
        if (source_node, target_node) not in self._edges:
            self._edges[(source_node, target_node)] = {}
        
        self._edges[(source_node, target_node)][edge] = metadata

    '''
    def _get_all_edges_between_two_nodes(self, source_node: str, target_node: str) -> Dict[str, Dict]:
        """
        Retrieves metadata for all edges between two nodes.

        Args:
            source_node (str): The starting node of the edges.
            target_node (str): The ending node of the edges.

        Returns:
            Dict[str, Dict]: A dictionary where keys are edge labels, 
            and values are metadata dictionaries.

        Example Output:
            {
                "knows": {
                    'fact_1234': {'fact_source': 'Wikipedia', 'confidence': 0.9},
                    'fact_1235': {'fact_source': 'Google Maps', 'confidence': 0.8}
                }
            }
        """
        return self._edges.get((source_node, target_node), {})
    
    def _list_of_edges(self) -> List[Dict[str, any]]:
        """
        Returns a list of all edges in the graph in the form of {'source_node': source_node, 'edge': edge, 'target_node': target_node, **metadata}
        """
        return [
            {
                "source_node": source_node,
                "edge": edge,
                "target_node": target_node,
                **{key: value for key, value in metadata.items() if key not in {'source_node', 'target_node', 'edge'}}
            }
            for ((source_node, target_node), edge_dict) in self._edges.items()    
            for edge, metadata in edge_dict.items()
        ]
    
    def _list_of_nodes(self) -> List[Dict[str, any]]:
        """
        Returns a list of all nodes in the graph.
        """
        return [
            {
                "node": node,
                **{key: value for key, value in metadata.items() if key != 'node'}
            }
            for node, metadata in self._nodes.items()
        ]
    '''

    def _out_edges(self, node: str) -> List[Tuple[str, str, Dict]]:
        """
        Retrieves all outgoing edges from a node.

        Args:
            node (str): The node to retrieve outgoing edges from.

        Returns:
            Dict[Tuple[str, str], Dict[str, Dict]]: A dictionary where keys are tuples of (source, target) and values are dictionaries of edges and their metadata.

        Example Output:
            {
                ("Alice", "Bob"): {"knows": metadata},
                ("Alice", "Charlie"): {"friend_of": metadata}
            }
        """
        return {
            (source_node, target_node): edges
            for (source_node, target_node), edges in self._edges.items() if source_node == node
        }

    def _in_edges(self, node: str) -> List[Tuple[str, str, Dict]]:
        """
        Retrieves all incoming edges to a node.

        Args:
            node (str): The node to retrieve incoming edges for.

        Returns:
            Dict[Tuple[str, str], Dict[str, Dict]]: A dictionary where keys are tuples of (source, target) and values are dictionaries of edges and their metadata.

        Example Output:
            {
                ("Bob", "Alice"): {"knows": metadata},
                ("Charlie", "Alice"): {"friend_of": metadata}
            }
        """
        return {
            (source_node, target_node): edges
            for (source_node, target_node), edges in self._edges.items() if target_node == node
        }

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
            return (source_node, target_node) in self._edges and bool(self._edges[(source_node, target_node)])
        else:
            return (source_node, target_node) in self._edges and edge in self._edges[(source_node, target_node)]

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
        if (source_node, target_node) in self._edges:
            if edge:
                if edge in self._edges[(source_node, target_node)]:
                    self._edges[(source_node, target_node)].pop(edge, None)
                    if self._edges[(source_node, target_node)] == {}:  # Remove entry if no edges remain
                        del self._edges[(source_node, target_node)]
                elif raise_if_not_found:
                    raise KeyError(f"Edge {edge} not found between {source_node} and {target_node}")
            else:
                if (source_node, target_node) in self._edges:
                    del self._edges[(source_node, target_node)]  # Remove all edges
                elif raise_if_not_found:
                    raise KeyError(f"No edge found between {source_node} and {target_node}")


    def _remove_node(self, node: str):
        """
        Removes a node from the graph along with all its connected edges.

        Args:
            node (str): The node to remove.

        Example:
            _remove_node("Alice")  # Removes Alice and all edges connected to Alice.
        """
        if node in self._nodes:
            del self._nodes[node]

        # Remove all edges where this node is either source or target
        self._edges = {(s, t): edges for (s, t), edges in self._edges.items() if s != node and t != node}

    def _get_edges(self, source_node: Optional[str] = None, target_node: Optional[str] = None, edge: Optional[str] = None) -> Dict[str, Dict]:
        """
        Retrieves metadata for all edges between two nodes.
        """
        if source_node is None and target_node is None:
            result = {}
            for (source_node, target_node), edges in self._edges.items():
                if edge is None:
                    result[(source_node, target_node)] = edges
                elif edge in edges:
                    result[(source_node, target_node)] = {edge: edges[edge]}
            return result

        if source_node is None or target_node is None:
            all_edges = self._in_edges(node=target_node) if source_node is None else self._out_edges(node=source_node)
            if edge is None:
                return all_edges
            else:
                return {
                    (source_node, target_node): {edge: all_edges_dict[edge]}
                    for (source_node, target_node), all_edges_dict in all_edges.items()
                    if edge in all_edges_dict
                }

        if edge is None:
            return {(source_node, target_node): self._edges[(source_node, target_node)]}
        else:
            return {(source_node, target_node): {edge: self._edges[(source_node, target_node)][edge]}}
        
    def _remove_edges(self, source_node: Optional[str] = None, target_node: Optional[str] = None, edge: Optional[str] = None, raise_if_not_found: bool = False):
        """
        Removes edges between two nodes. If no specific edge label is provided, all edges between
        the nodes are removed.
        
        
        """
        if source_node is None and target_node is None and edge is None:
            self._edges = {}
            self._nodes = {}
            return
        elif source_node is not None and target_node is not None:
            return self._remove_edge(source_node=source_node, target_node=target_node, edge=edge, raise_if_not_found=raise_if_not_found)
        else:
            all_edges = self._get_edges(source_node=source_node, target_node=target_node, edge=edge)
            for (_source_node, _target_node), edges in all_edges.items():
                if source_node is not None and _source_node != source_node:
                    continue
                if target_node is not None and _target_node != target_node:
                    continue
                self._remove_edge(source_node=_source_node, target_node=_target_node, edge=edge, raise_if_not_found=raise_if_not_found)
            return

    _delete_edges = _remove_edges

    def _clear_graph(self):
        """
        Removes all nodes and edges from the graph.

        Example:
            _clear_graph()  # Completely resets the graph.
        """
        self._nodes.clear()
        self._edges.clear()

    def _n_edges(self) -> int:
        """
        Returns the number of edges in the graph.
        """
        return len(self._edges)

    def _copy(self) -> 'SimpleGraphBackend':
        """
        Returns a copy of the graph.
        """
        new_graph_backend = SimpleGraphBackend()
        new_graph_backend._nodes = self._nodes.copy()
        new_graph_backend._edges = self._edges.copy()
        return new_graph_backend

