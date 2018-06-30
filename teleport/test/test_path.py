from ..graph import CityNode
from ..path import Path


class TestPath:
    def test_add_method(self):
        # test adding to Path Objects
        path1 = Path([CityNode('a'), CityNode('b')])
        path2 = Path([CityNode('c'), CityNode('d')])

        path = path1 + path2
        assert 4 == len(path.data)
        assert ['a', 'b', 'c', 'd'] == [cn.name for cn in path.data]

        # test adding a Path with a CityNode
        path = Path([CityNode('a'), CityNode('b')])
        path = path + CityNode('c')

        assert 3 == len(path.data)
        assert ['a', 'b', 'c'] == [cn.name for cn in path.data]

    def test_is_loop(self):
        # start and end nodes don't match
        assert False is Path([CityNode('a'), CityNode('b'), CityNode('c')]).is_loop()

        # test only one node between start and end
        # is_loop only checks for object equality - so we can use strings for matching in this case
        assert False is Path(['a', 'b', 'a']).is_loop()

        # a valid loop
        assert True is Path(['a', 'b', 'd', 'a']).is_loop()

        # another one
        assert True is Path(['a', 'b', 'd', 'e', 'f', 'a']).is_loop()

        # an invalid loop
        assert False is Path(['a', 'b', 'd', 'e', 'b', 'a']).is_loop()

