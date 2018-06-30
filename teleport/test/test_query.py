from ..query import find_nearby_cities, does_route_exist, does_loop_exist
from ..graph import TeleportGraph


class TestFindNearbyCities:
    def test_hop_levels(self, basic_graph: TeleportGraph):
        """
        :param basic_graph: a TeleportGraph supplied as a test fixture - defined in conftest.py
        :return:
        """
        cities = find_nearby_cities(basic_graph, city='Seattle', num_hops=0)
        assert 0 == len(cities)

        cities = find_nearby_cities(basic_graph, city='Seattle', num_hops=1)
        assert 2 == len(cities)
        assert {'Baltimore', 'New York'} == {city for city in cities}

        cities = find_nearby_cities(basic_graph, city='Seattle', num_hops=2)
        assert 4 == len(cities)
        assert {'Baltimore', 'New York', 'Washington', 'Philadelphia'} == {city for city in cities}


class TestDoesRouteExist:
    def test_valid_route_requests(self, basic_graph: TeleportGraph):
        """
        :param basic_graph: a TeleportGraph supplied as a test fixture - defined in conftest.py
        :return:
        """
        assert True is does_route_exist(basic_graph, 'New York', 'Atlanta')
        assert False is does_route_exist(basic_graph, 'Oakland', 'Atlanta')


class TestDoesLoopExist:
    def test_loop_existence(self, basic_graph: TeleportGraph):
        """
        :param basic_graph:
        :return:
        """
        assert True is does_loop_exist(basic_graph, 'Oakland')
        assert False is does_loop_exist(basic_graph, 'Washington')
        assert True is does_loop_exist(basic_graph, 'Baltimore')
