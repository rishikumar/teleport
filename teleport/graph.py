from collections import namedtuple
from .error import DataException


Route = namedtuple('Route', ['start', 'end'])


class CityNode:
    """Represents a node in the TeleportGraph"""
    def __init__(self, name):
        self._name = name
        self._related_cities = set()

    @property
    def name(self):
        return self._name

    @property
    def related_cities(self):
        return self._related_cities

    def add_related_city(self, city):
        self._related_cities.add(city)

    def remove_related_city(self, city):
        self._related_cities.remove(city)

    def __repr__(self):
        return f"{self.__class__.name}(name={self.name})"


class TeleportGraph:
    """Represents the graph data structure - contains an index (via a dict) to each node"""
    def __init__(self):
        self._city_nodes = dict()

    @property
    def city_nodes(self):
        return self._city_nodes.values()

    @classmethod
    def from_tuples(cls, routes):
        """
        Build a new graph based upon the provided routes
        :param routes: the routes to add to the newly created graph
        :return: the constructed graph
        """
        instance = cls()

        for city1, city2 in routes:
            instance.add_route(city1, city2)

        return instance

    def add_route(self, city1, city2):
        """
        Adds a new bi-directional route to the graph, given string representations of the cities it connects.
        :param city1: A city and one endpoint of the route
        :param city2: A city and one endpoint of the graph
        :return: None
        """
        node1 = self._get_or_create_node(city1)
        node2 = self._get_or_create_node(city2)

        # explicitly add the link relationship between the two cities
        node1.add_related_city(node2)
        node2.add_related_city(node1)

    def find_city_node(self, name) -> CityNode:
        """
        Locates a given CityNode in the graph based upon the provided name. If the node is not found,
        an exception is raised
        :param name: The name of the city to query for
        :return: The requested CityNode object
        """
        try:
            return self._city_nodes[name]
        except KeyError as e:
            raise DataException(f"Could not locate a city node in the graph for city=[{city}]") from e

    def _get_or_create_node(self, city):
        """
        Locates the city node with the name specified by the city argument - if not found, it will create a new one
        :param city: name of the city to get/create
        :return: A CityNode object
        """
        if city not in self._city_nodes:
            self._city_nodes[city] = CityNode(city)

        return self._city_nodes[city]
