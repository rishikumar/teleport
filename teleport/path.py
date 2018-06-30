from collections import Iterable
from copy import copy


class Path:
    """Represents the traversal of nodes along edges in the graph"""
    def __init__(self, data=None):
        self._stack = list()

        # depending upon the type of data we're passed, we determine which "push" function to use - extend vs append
        if data is not None:
            push_fn = self._stack.extend if isinstance(data, Iterable) else self._stack.append
            push_fn(data)

    @property
    def data(self):
        return self._stack

    def __add__(self, other):
        """
        Uses to provide the following operators:
        Path + CityNode
        Path + Path
        Path + [CityNode, CityNode, ...]
        """
        # shallow copy of the stack of this object since we're not modifying any of its objects, just appending
        # a new item to the newly created path object
        stack = copy(self._stack)

        # handling 3 types of input: another Path object, a iterable of nodes and a single node
        if isinstance(other, Path):
            stack.extend(other._stack)
        elif isinstance(other, Iterable):
            stack.extend(other)
        else:
            stack.append(other)

        return Path(stack)

    def is_loop(self):
        """
        Determines if the path of this object is a valid loop - e.g. if the same route is not used twice in the loop
        :return: bool
        """
        nodes = self._stack

        if len(nodes) < 4:
            # cannot have a loop in this case
            return False

        # start and end nodes should match
        if nodes[0] != nodes[-1]:
            return False

        # Other than the start and end nodes, all nodes should be unique
        inner_nodes = nodes[1:-1]
        return len(inner_nodes) == len(set(inner_nodes))