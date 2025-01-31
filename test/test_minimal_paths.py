import unittest
import datetime
from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType



class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    cn1 = CommunicationNetwork({'1': {"participant 1", "participant 2", "participant 3"}},{'1': datetime.datetime(2023,6,1,10,10,10)})

    def test_shortest_path_tc1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_equal_output_shortest_tc2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_equal_output_fastest_tc3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_equal_output_foremost_tc4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')


    def test_hedges_shortest_path_tc5(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,"participant 1", DistanceType.SHORTEST, datetime.datetime(1,1,1,0,0))
        expected_res = {"participant 3" : 1,"participant 2": 1}
        self.assertEqual(result, expected_res)

    def test_vertex_shortest_path_tc6(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,"participant 1", DistanceType.SHORTEST, datetime.datetime(1,1,1,0,0))
        expected_res = {'participant 2': 1, 'participant 3': 1}
        self.assertEqual(result, expected_res)


    def test_vertex_fastest_path_tc7(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,"participant 1", DistanceType.FASTEST, datetime.datetime(2023,6,1,10,10,10))
        expected_res = {"participant 3" : datetime.timedelta(0),"participant 2": datetime.timedelta(0)}
        self.assertEqual(result, expected_res)

    def test_hedges_fastest_path_tc8(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,"participant 1", DistanceType.FASTEST, datetime.datetime(2023,6,1,10,10,10))
        expected_res = {"participant 3": datetime.timedelta(0), "participant 2": datetime.timedelta(0)}
        self.assertEqual(result, expected_res)

    def test_hedges_foremost_path_tc9(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,"participant 1", DistanceType.FOREMOST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {"participant 3" :datetime.datetime(2023,6,1,10,10,10),"participant 2": datetime.datetime(2023,6,1,10,10,10)}
        self.assertEqual(result, expected_res)

    def test_vertex_foremost_path_tc10(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,"participant 1", DistanceType.FOREMOST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {"participant 3" :datetime.datetime(2023,6,1,10,10,10),"participant 2": datetime.datetime(2023,6,1,10,10,10)}
        self.assertEqual(result, expected_res)
