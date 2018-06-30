# Teleportation

## Getting it Running

####Via python 3.6

The main script has one command line option called `input_path` - this is the location of the input text file.  

An example is created in the `teleport/data` directory. Here is an example execution of the script from the root directory of the project.

````sh
python teleport.py --input-path=teleport/data/teleport_input_sample_1.txt
````



####Via Docker

The project is also setup to run with docker compose. To get docker docker-compose up and running, please refer to the the online documentation for these projects. 

Building the container (from the root directory of the project):

```sh
docker build -t teleport .
```

Running the app

```sh
docker run teleport python teleport.py --input-path=teleport/data/teleport_input_sample_1.txt
```



To run new data files in the docker container, add the files into the `teleport/data` folder and rebuild the continer.



## Running Tests

Unit tests can be run by using `pytest` - to add this package to your python environment, you can run the following:

```sh
pip install -r requirements.txt
```

All tests can be run with the following command from the project root projectory:

```sh
pytest
```

### Running tests in docker

```sh
docker run teleport pytest
```



## Application Design

The application models the telegraph data into a graph (the `TeleportGraph`) in which the nodes are represented by `CityNode` objects. The routes (e.g. edges) between the nodes are stored in the `CityNode` objects as a set of related cities. 

The application is broken into several components. They are mentioned here in the order in which they are encountered in the execution of the application:

- `teleport.py` - this is the main script of the application. It takes in the location of an input file and produces the application's output to the command line
- `parser.py` - The parser is responsible for parsing the input file and building two lists from it. It builds a list of routes to load into the graph and a list of functions to execute to query a graph. The function list is pre-configured with the metadata from the queries in the text file and they only require a graph upon which to operate.
- `query.py` - this module contains the querying functions - they are: `find_nearby_cities`, `does_route_exist`, `does_loop_exist` - these functions have no knowledge of input and output formats - that scaffolding is handled by the helper methods in `parser.py`
- `graph.py` - Contains the `CityNode` and `TeleportGraph` model classes, which are essentially containers for the graph relationships
- `path.py` - contains the Path model class, which is used as pat of the `does_loop_exist` algorithm

Tests have been created to test various application scenarios - they are in the `teleport/test` directory



### Assumptions

I've made some assumptions during the creation of my solution:

-  The names of cities are case-sensitive and can include any alphanumeric character.  See `teleport.parser.InputParser` for the regular expressions I'm using to parse the input file
-  The code will ignore input files that don't match the regular expressions defined in `teleport.parser.InputParser`.
-  Self-referential and duplicate routes will be ignored and will not raise an exception: 





