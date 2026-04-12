import pytest
from .webtris_graph import Graph, calc_path_weight, dfs, bfs


class Test_Graph_Class:
    ''' Tests for the Graph class such as node and edge creation and any error handling '''
    @pytest.fixture
    def simple_graph(self):
        g = Graph({})
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edges("A", "B", 5)
        g.add_edges("B", "D", 10)
        g.add_edges("B", "C", 3)
        g.add_edges("C", "D", 2)
        return g

    def test_add_node_and_edges(self, simple_graph):
        roads_a = simple_graph.get_all_roads("A")
        assert "B" in roads_a
        assert roads_a["B"] == 5

        roads_c = simple_graph.get_all_roads("C")
        assert "D" in roads_c
        assert roads_c["D"] == 2
    
    def test_returns_all_nodes(self, simple_graph):
        roads = simple_graph.road_system
        assert set(roads) == {"A", "B", "C", "D"}
        assert set(roads) != {"A", "B", "C", "E"}

    def test_add_missing_edges(self):
        g = Graph({})
        g.add_node("A")
        with pytest.raises(Exception):
            g.add_edges("A", "Z", 10)

class Test_Calc_Path_Weight:
    @pytest.fixture
    def simple_graph(self):
        g = Graph({})
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edges("A", "B", 5)
        g.add_edges("B", "D", 10)
        g.add_edges("B", "C", 3)
        g.add_edges("C", "D", 2)
        return g

    def test_path_weight(self, simple_graph):
        path = ["A", "B", "C", "D"]
        assert calc_path_weight(simple_graph, path) == 10
    
    def test_edge_weight(self, simple_graph):
        path = ["A", "B"]
        assert calc_path_weight(simple_graph, path) == 5

    def test_one_node_weight(self, simple_graph):
        path = ["A"]
        assert calc_path_weight(simple_graph, path) == 0

class Test_BFS:
    ''' Tests for breatdth first search. Should find the path with the fewest amount of steps '''
    @pytest.fixture
    def simple_graph(self):
        g = Graph({})
        g.add_node("A")
        g.add_node("B")
        g.add_node("C")
        g.add_node("D")
        g.add_edges("A", "B", 5)
        g.add_edges("B", "D", 10)
        g.add_edges("B", "C", 3)
        g.add_edges("C", "D", 2)
        return g
    
    def test_bfs_fewest_steps(self, simple_graph):
        ''' BFS from A to D should return A->B->D not A->B->C->D which is longer '''
        path, time = bfs(simple_graph, "A", "D")
        assert path == ["A", "B", "D"]
        assert time == 15 #BFS Does not care about weigjt so it should return 15 insstead of the cheaper route which is only 10
    
    def test_bfs_start_sameAs_end(self, simple_graph):
        '''When the start and end node are the same, BFS should return time as 0 '''
        path, time = bfs(simple_graph, "A", "A")
        assert path == ["A"]
        assert time == 0