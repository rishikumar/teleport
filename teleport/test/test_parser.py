import io
from ..parser import InputParser


class TestInputParser:
    def test_route_parsing(self, basic_routes):
        stream = io.StringIO(basic_routes)
        data = InputParser.from_stream(stream)

        assert 3 == len(data.routes)

    def test_invalid_route(self):
        # Confirm that invalid route data gets ignored
        route_text = """
        City -
        - City
        City City
        
        """

        stream = io.StringIO(route_text)
        data = InputParser.from_stream(stream)
        assert 0 == len(data.routes)

        # Valid routes are kept and invalid ones are ignored
        route_text = """
        City - 
        
        City1 - City2
        - City
        """

        stream = io.StringIO(route_text)
        data = InputParser.from_stream(stream)
        assert 1 == len(data.routes)

    def test_query_parsing(self, basic_queries):
        stream = io.StringIO(basic_queries)
        data = InputParser.from_stream(stream)

        assert 3 == len(data.queries)

    def test_invalid_query_data(self):
        # Confirm that invalid query commands get ignored
        query_text = """
            My random command
            loop possible City 
        """
        stream = io.StringIO(query_text)
        data = InputParser.from_stream(stream)
        assert 0 == len(data.queries)

        # Valid queries are kept and invalid ones are ignored
        query_text = """
            My random command
            cities from City in 1 jumps 
            loop possible City 
            can I teleport from X to Y
        """

        stream = io.StringIO(query_text)
        data = InputParser.from_stream(stream)
        assert 2 == len(data.queries)
