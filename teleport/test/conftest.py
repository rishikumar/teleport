import pytest

from ..graph import TeleportGraph, Route


@pytest.fixture
def basic_graph():
    routes = [
        Route(start='Washington', end='New York'),
        Route(start='Washington', end='Atlanta'),
        Route(start='Baltimore', end='Philadelphia'),
        Route(start='Philadelphia', end='New York'),
        Route(start='Los Angeles', end='San Fransisco'),
        Route(start='San Fransisco', end='Oakland'),
        Route(start='Los Angeles', end='Oakland'),
        Route(start='Seattle', end='New York'),
        Route(start='Seattle', end='Baltimore')
    ]

    graph = TeleportGraph.from_tuples(routes)
    return graph


@pytest.fixture
def basic_routes():
    return \
        """A - B
        AAAAA - BBBBB
        A A A - B B B"""


@pytest.fixture
def basic_queries():
    return \
        """cities from Seattle in 1 jumps
        can I teleport from New York to Atlanta
        loop possible from Oakland"""
