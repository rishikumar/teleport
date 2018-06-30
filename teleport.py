import argparse

from teleport.parser import InputParser
from teleport.graph import TeleportGraph


def main():
    """
    Main execution function for the script.
    This is done in a method to scope the variables locally (instead of polluting the module namespace)
    :return:
    """
    args = _get_argument_parser().parse_args()

    # read the file and interpret its contents
    data = InputParser.from_path(args.input_path)

    # build the graph
    graph = TeleportGraph.from_tuples(data.routes)

    # execute queries and print results
    for query in data.queries:
        result = query(graph)
        print(result)


def _get_argument_parser():
    """
    Builds the object that handles the command line arguments
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="This script builds the teleportation "
                                                 "graph and executes queries against it")

    # add argument(s) to the parser
    parser.add_argument('--input-path',
                        dest='input_path',
                        required=True,
                        help="fully qualified path to the input file")

    return parser


if __name__ == '__main__':
    main()
