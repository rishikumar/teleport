import re
from functools import partial
from .query import find_nearby_cities, does_route_exist, does_loop_exist
from .graph import Route, TeleportGraph


# query translation methods
def render_nearby_city_query(match):
    """
    This method is invoked in response to a user query. It returns a partially built function that includes the input
    arguments from the parsed input text that can be applied to any graph. It also renders the output format
    :param match: the regular expression object that has the parsed input data
    :return: fully rendered response
    """

    def invoke_and_render(graph: TeleportGraph, city, num_hops):
        results = find_nearby_cities(graph, city=city, num_hops=num_hops)
        return f"cities from {city} in {num_hops} hops: {', '.join(results)}"

    return partial(invoke_and_render, city=match.group(1), num_hops=int(match.group(2)))


def render_does_route_exist(match):
    """
    This method is invoked in response to a user query. It returns a partially built function that includes the input
    arguments from the parsed input text that can be applied to any graph. It also renders the output format
    :param match: the regular expression object that has the parsed input data
    :return: fully rendered response
    """
    def invoke_and_render(graph: TeleportGraph, start_city, end_city):
        result = does_route_exist(graph, start_city, end_city)
        result_msg = 'yes' if result else 'no'
        return f"can I teleport from {start_city} to {end_city}: {result_msg}"

    return partial(invoke_and_render, start_city=match.group(1), end_city=match.group(2))


def render_does_loop_exist(match):
    """
    This method is invoked in response to a user query. It returns a partially built function that includes the input
    arguments from the parsed input text that can be applied to any graph. It also renders the output format
    :param match: the regular expression object that has the parsed input data
    :return: fully rendered response
    """
    def invoke_and_render(graph: TeleportGraph, city):
        result = does_loop_exist(graph, city)
        result_msg = 'yes' if result else 'no'
        return f"loop possible from {city}: {result_msg}"

    return partial(invoke_and_render, city=match.group(1))


class InputParser:
    """Processes streams of input, parses the entries into routes and queries"""
    # capture groups that match '<city> - <city>' where <city> can be any alphanumeric character or a space
    ROUTE_PATTERN = re.compile('([\w\s]*) - ([\w\s]*)')

    # query patterns:
    NEARBY_CITIES_PATTERN = re.compile('cities from ([\w\s]*) in ([\d]) jumps')
    DOES_ROUTE_EXIST_PATTERN = re.compile('can I teleport from ([\w\s]*) to ([\w\s]*)')
    DOES_LOOP_EXIST_PATTERN = re.compile('loop possible from ([\w\s]*)')

    PATTERN_TRANSLATER_MAP = {
        NEARBY_CITIES_PATTERN: render_nearby_city_query,
        DOES_ROUTE_EXIST_PATTERN: render_does_route_exist,
        DOES_LOOP_EXIST_PATTERN: render_does_loop_exist
    }

    def __init__(self):
        self._routes = list()
        self._queries = list()

    @property
    def routes(self):
        return self._routes

    @property
    def queries(self):
        return self._queries

    @classmethod
    def from_path(cls, input_path: str):
        """
        Processes the input_file and build collections of routes and queries
        :param input_path: fully qualified path to the file
        :return: the generated instances
        """
        with open(input_path, mode='r', encoding='utf-8') as f:
            return cls.from_stream(f)

    @classmethod
    def from_stream(cls, stream):
        """
        Processes the text stream and build collections of routes and queries
        :param stream: input file stream
        :return: the generated instances
        """
        instance = cls()

        for line in stream:
            line = line.strip()
            # process routes in the file
            route = instance._parse_route(line)
            if route:
                instance._routes.append(route)
                continue

            # process queries
            query = instance._parse_query(line)
            if query:
                instance._queries.append(query)

        return instance

    def _parse_route(self, entry):
        """
        Parse the route string text
        :param entry: input command
        :return:
        """
        match = self.ROUTE_PATTERN.fullmatch(entry)
        if match:
            return Route(start=match.group(1), end=match.group(2))

    def _parse_query(self, entry):
        """
        Parses query commands based upon the patterns in PATTERN_TRANSLATER_MAP
        :param entry: input command
        :return:
        """
        for pattern in self.PATTERN_TRANSLATER_MAP.keys():
            match = pattern.fullmatch(entry)
            if match:
                translation_fn = self.PATTERN_TRANSLATER_MAP[pattern]
                return translation_fn(match)

