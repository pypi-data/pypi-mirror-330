from .BaseGraphBackend import BaseGraphBackend
from typing import Optional, List, Tuple, Dict, Union, Literal, Callable
from collections import deque
from atlantis.utils import has_circular_reference
from datetime import datetime
from .exceptions import GraphBackendDeprication


# DEPRECATED: To be removed in the next major release
def _metadata_is_valid(metadata: Union[Dict, None]) -> bool:
    """
    Metadata cannot contain the same key in multiple layers
    Metadata cannot have more than 3 layers of depth
    """
    raise GraphBackendDeprication("This method is deprecated. Use the validate_metadata method instead.")
    def _get_depth(obj):
        items = [obj]
        depth = -1
        while len(items) > 0:
            depth += 1
            new_items = []
            for x in items:
                if isinstance(x, (dict, tuple, list, set)):
                    if len(x) == 0:
                        new_items.append(None)
                    elif isinstance(x, dict):
                        new_items += list(x.keys())
                        new_items += list(x.values())
                    else:
                        new_items += list(x)
            items = new_items
        return depth
    
    def _has_duplicate_keys(dictionary):
        items = [dictionary]
        all_keys = set()
        while len(items) > 0:
            new_items = []
            for item in items:
                for key, value in item.items():
                    if key in all_keys:
                        return True
                    all_keys.add(key)
                    if isinstance(value, dict):
                        new_items.append(value)
            items = new_items
        return False

    if metadata is None:
        return (True, 'Metadata is None')
    if not isinstance(metadata, dict):
        return (False, 'Metadata is not a dictionary')
    
    if _get_depth(metadata) > 3:
        return (False, 'Metadata has more than 3 layers of depth')
    
    if _has_duplicate_keys(metadata):
        return (False, 'Metadata has duplicate keys')
    
    return (True, 'Metadata is valid')

class GraphBackend(BaseGraphBackend):
    """
    The public API for the graph backend that uses the abstract base class 
    and provides the standard methods that are not supposed to be changed by the subclasses.
    The subclasses should implement:
    - _has_node
    - _add_node
    - _add_edge
    - _get_edges
    - _has_edge
    - _remove_edge
    - _remove_edges
    """

    def copy(self, **kwargs) -> 'GraphBackend':
        """
        Returns a copy of the graph.
        """
        return self._copy(**kwargs)

    @property
    def data_dict(self) -> Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]:
        """
        Gets the data dictionary of the graph backend.
        """
        return self._data_dict

    def validate_metadata(self, metadata: Dict) -> bool:
        """
        Validates the metadata.
        """
        raise GraphBackendDeprication("This method is deprecated. Use the validate_metadata method instead.")
        is_valid, reason = self.metadata_validation_function(metadata)
        if not is_valid:
            raise RuntimeError(f"Metadata: {metadata} is not valid because: {reason}")

    def add_edge(self, source_node: str, edge: str, target_node: str, metadata: Optional[Dict] = {}):
        """
        Adds a directed edge between two nodes.

        Args:
            source_node (str): The starting node.
            edge (str): The edge type.
            target_node (str): The ending node.
            metadata: Additional metadata to associate with the edge.
        """

        if not self._has_node(source_node):
            self._add_node(source_node)
        if not self._has_node(target_node):
            self._add_node(target_node)

        self._add_edge(source_node=source_node, target_node=target_node, edge=edge, metadata=metadata)

    def get_edges(self, source_node: str, target_node: str, edge: Optional[str] = None) -> Dict[Tuple[str, str], Dict[str, Dict]]:
        """
        Retrieves all edges between two nodes.


        Args:
            source_node (str): The starting node.
            target_node (str): The ending node.

        Returns:
            Dict[Tuple[str, str], Dict[str, Dict]]: A dictionary where keys are tuples of (source_node, target_node) and values are dictionaries of edges and their metadata.

        Example Output:
        {
            (source_node_1, target_node_1): {edge_1: metadata_1, edge_2: metadata_2, ...},
            (source_node_2, target_node_2): {edge_1: metadata_1, edge_2: metadata_2, ...},
            ...
        }
        """
        return self._get_edges(source_node=source_node, target_node=target_node, edge=edge)
    
    def has_edge(self, source_node: str, target_node: str, edge: Optional[str] = None) -> bool:
        """
        Checks if an edge exists between two nodes.
        """
        return self._has_edge(source_node=source_node, target_node=target_node, edge=edge)
    
    def has_node(self, node: str) -> bool:
        """
        Checks if a node exists in the graph.
        """
        return self._has_node(node=node)

    def remove_edge(self, source_node: str, target_node: str, edge: Optional[str] = None):
        """
        Removes an edge between two nodes. If no specific edge type is provided, all edges between
        the nodes are removed.

        Args:
            source_node (str): The starting node.
            target_node (str): The ending node.
            edge (Optional[str]): The specific edge type to remove. If None, all edges are removed.
        
        """
        if self._has_edge(source_node=source_node, target_node=target_node):
            self._remove_edge(source_node=source_node, target_node=target_node, edge=edge)

    delete_edge = remove_edge

    def remove_edges(
            self,
            source_node: Optional[str] = None,
            edge: Optional[str] = None,
            target_node: Optional[str] = None
        ):
        """
        Removes edges from the graph backend.
        """
        return self._remove_edges(source_node=source_node, edge=edge, target_node=target_node)
    
    delete_edges = remove_edges

    def remove_node(self, node: str):
        """
        Removes a node and all its edges.

        Args:
            node (str): The node to remove.
        """
        # Retrieve all edges before modifying the graph
        out_edges = [(node, target_node, edge) for _, target_node, edge in self._out_edges(node)]
        in_edges = [(source_node, node, edge) for source_node, _, edge in self._in_edges(node)]
        
        # Remove all edges
        for source_node, target_node, edge in out_edges:
            self._remove_edge(source_node=source_node, target_node=target_node, edge=edge)
        for source_node, target_node, edge in in_edges:
            self._remove_edge(source_node=source_node, target_node=target_node, edge=edge)

        # Remove the node itself
        self._remove_node(node)
    
    delete_node = remove_node

    def clear(self):
        """
        Clears all nodes and edges from the graph.

        Example:
            clear()  # Completely resets the graph.
        """
        self._clear_graph()

    # DEPRECATED: To be removed in the next major release
    def get_neighbours(
        self, node: str, depth: int = 1, direction: str = "outgoing",
        output_format: Optional[Union[str, Tuple[str, ...]]] = ('source_node', 'edge', 'target_node'),
        return_as_dict: bool = False
    ) -> List[Tuple]:
        raise GraphBackendDeprication("This method is deprecated. Use the get_neighbours method instead.")
        """
        Retrieves all neighbors of a node up to a certain depth using BFS.

        Args:
            node (str): The starting node.
            depth (int): The maximum depth to search.
            direction (str): 'outgoing', 'incoming', or 'both'.
            output_format (tuple): Output format options:
                - ('target_node', 'edge') (default)
                - ('source_node', 'edge', 'target_node')
                - ('source_node', 'edge', 'target_node', 'metadata')
            return_as_dict (bool): If True, return a dictionary of neighbours.

        Returns:
            List[Tuple]: List of tuples containing requested fields.
        """
        if not self._has_node(node):
            return []

        queue = deque([(node, 0)])
        visited = {node}
        neighbours = {}

        while queue:
            current_node, _current_depth = queue.popleft()
            if _current_depth >= depth:
                continue

            next_nodes = []
            if direction in ["outgoing", "both"]:
                next_nodes.extend(self._out_edges(current_node))

            if direction in ["incoming", "both"]:
                next_nodes.extend(self._in_edges(current_node))

            for source_node, target_node, data in next_nodes:
                edge = data.get("edge", "unknown")
                depth_increment = self.depth_exceptions.get(edge, 1)
                next_depth = _current_depth + depth_increment

                # Determine the correct neighbor based on direction
                if direction == 'incoming':
                    neighbour_nodes = [source_node]
                elif direction == 'outgoing':
                    neighbour_nodes = [target_node]
                else:
                    neighbour_nodes = [source_node, target_node]

                # Ensure correct tuple ordering
                formatted_entry = self._format_output(source_node=source_node, target_node=target_node, data=data, output_format=output_format, depth=next_depth)
                key = (source_node, edge, target_node)

                if key not in neighbours:
                    neighbours[key] = (next_depth, formatted_entry)
                else:
                    _next_depth, _ = neighbours[key]
                    if next_depth < _next_depth:
                        neighbours[key] = (next_depth, formatted_entry)

                # Mark neighbor as visited before enqueuing to avoid duplicate processing
                for neighbour in neighbour_nodes:
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append((neighbour, next_depth))

        if return_as_dict:
            return {key: formatted_entry for key, (_, formatted_entry) in neighbours.items()}
        return [formatted_entry for depth, formatted_entry in neighbours.values()]

    # DEPRECATED: To be removed in the next major release
    def get_list_of_edges(self) -> List[Dict[str, any]]:
        """
        Returns a list of all edges in the graph in the form of {'source_node': source_node, 'edge': edge, 'target_node': target_node, **metadata}
        """
        raise GraphBackendDeprication("This method is deprecated. Use the list_of_edges property instead.")
        return self._list_of_edges()
    
    # DEPRECATED: To be removed in the next major release
    @property
    def edges(self) -> List[Dict[str, any]]:
        """
        Returns a list of all edges in the graph in the form of {'source_node': source_node, 'edge': edge, 'target_node': target_node, **metadata}
        """
        raise GraphBackendDeprication("This property is deprecated. Use the list_of_edges property instead.")
        return self._list_of_edges()
    
    # DEPRECATED: To be removed in the next major release
    @property
    def nodes(self) -> List[Dict[str, any]]:
        """
        Returns a list of all nodes in the graph in the form of {'node': node, **metadata}
        """
        raise GraphBackendDeprication("This property is deprecated. Use the list_of_nodes property instead.")
        return self._list_of_nodes()


