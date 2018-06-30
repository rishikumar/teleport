from queue import Queue

from .graph import TeleportGraph, CityNode
from .path import Path


def find_nearby_cities(graph: TeleportGraph, city: str, num_hops: int = 1) -> set:
    """
    This function locates all nearby cities within num_hops from the given city. It maintains a set of all the cities
    visited from the starting city at each hop. After completion, it removes the original city from the list of results
    :param graph: the graph to query
    :param city: the starting point for the search
    :param num_hops: the number of hops to execute to locate nearby cities
    :return: set of all cities that match
    """

    if num_hops == 0:
        return set()

    start_city_node = graph.find_city_node(city)

    city_nodes = {start_city_node}

    for i in range(num_hops):
        related_cities = set()

        # for every city in the current set, find all its related cities and add them to the global list of cities
        for city in city_nodes:
            related_cities |= city.related_cities

        city_nodes |= related_cities

    # The starting city cannot be near itself. It will always be added to the set because we have
    # bi-directional (undirected) edges between cities.
    city_nodes.remove(start_city_node)
    return {city.name for city in city_nodes}


def does_route_exist(graph: TeleportGraph, start_city: str, end_city: str) -> bool:
    """
    This function determines if two cities can be reached in the graph. This algorithm uses a breadth-first
    search approach
    :param graph: the graph to query
    :param start_city: the starting city
    :param end_city: the destination city
    :return: True if a route is found, False otherwise
    """
    queue = Queue()

    start_city_node = graph.find_city_node(start_city)
    queue.put(start_city_node)

    # keep track of the nodes we've visited - if we do not do this, we'll wind up in an infinite loop because since
    # we're dealing with an undirected graph
    visited_nodes = {start_city_node}

    while not queue.empty():
        city = queue.get()

        # if we've found the matching city - a route exists. no need to continue processing
        if city.name == end_city:
            return True

        # if not, let's check the related cities, only checking the cities we haven't visited already
        for related_city in city.related_cities:
            if related_city not in visited_nodes:
                visited_nodes.add(related_city)
                queue.put(related_city)

    return False


def does_loop_exist(graph: TeleportGraph, city: str) -> bool:
    """
    This function uses a closure to wrap the is_loop function in the context it needs to execute. It builds a Path
    object by traversing the tree in a depth-first search-like manner. The Path object itself is a stack, with the
    latest node in the path on the top
    :param graph: the graph to query
    :param city: the origin/destination city for the loop
    :return: bool
    """
    start_node = graph.find_city_node(city)
    visited_inner_nodes = set()

    def is_loop(path: Path, node: CityNode) -> bool:
        # check the current path + node combination to see if they form a loop
        new_path = path + node

        if node != start_node and node not in visited_inner_nodes:
            visited_inner_nodes.add(node)

        if new_path.is_loop():
            return True

        # If we've not found a loop yet, let's check the related nodes of this node and call ourselves recursively
        # get the set of nodes for the candidates in the path. This list comprehension filters out related nodes that
        # point back to the last entry on the path to avoid backtracking along the same nodes back to the origin
        # path_candidates = path.get_directed_path_nodes(node.related_cities)
        path_candidates = [rc for rc in node.related_cities
                           if rc not in visited_inner_nodes and rc not in path.data[-1:]]
        for pc in path_candidates:
            # check to see if the path candidate, in combination with the current path object form a loop
            if is_loop(new_path, pc):
                return True

        # the current path and all its descendants do not form a loop
        return False

    return is_loop(Path(), start_node)




