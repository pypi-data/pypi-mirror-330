class GraphBackendException(Exception):
    """
    Base class for all exceptions in the graph backend.
    """
    pass

class GraphBackendDeprication(GraphBackendException):
    """
    Exception raised when a method is deprecated.
    """
    pass
