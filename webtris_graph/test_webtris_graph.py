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
