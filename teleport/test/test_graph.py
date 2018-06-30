from ..graph import CityNode, TeleportGraph


class TestCityNode:
    def test_initialization(self):
        cn = CityNode('a')

        b = CityNode('b')
        c = CityNode('c')

        cn.add_related_city(b)
        cn.add_related_city(c)

        assert {b, c} == cn.related_cities

        cn.remove_related_city(b)

        assert {c} == cn.related_cities


class TestTeleportGraph:
    def test_initialization(self):
        routes = [('a', 'b'),
                  ('b', 'c')]

        graph = TeleportGraph.from_tuples(routes)

        assert {'a', 'b', 'c'} == {cn.name for cn in graph.city_nodes}

        graph.add_route('c', 'd')
        graph.add_route('e', 'f')

        assert {'a', 'b', 'c', 'd', 'e', 'f'} == {cn.name for cn in graph.city_nodes}
