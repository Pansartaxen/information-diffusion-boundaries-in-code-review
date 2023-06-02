import unittest
import datetime
from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType



class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    cn1 = CommunicationNetwork({'-1000045392462314428': {-6410414390854871141, -4790071369877151138}},{'-1000045392462314428': datetime.datetime(2020,2,5,12,49,39)})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')


    def test_5(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,-6410414390854871141, DistanceType.SHORTEST, datetime.datetime(1,1,1,0,0))
        expected_res = {-4790071369877151138: 1}
        self.assertEqual(result, expected_res)

    def test_6(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,-6410414390854871141, DistanceType.SHORTEST, datetime.datetime(1,1,1,0,0))
        expected_res = {-4790071369877151138: 1}
        self.assertEqual(result, expected_res)


    def test_7(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,-6410414390854871141, DistanceType.FASTEST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {-4790071369877151138: datetime.timedelta(0)}
        self.assertEqual(result, expected_res)

    def test_8(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,-6410414390854871141, DistanceType.FASTEST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {-4790071369877151138: datetime.timedelta(0)}
        self.assertEqual(result, expected_res)
        
    def test_9(self):
        result = single_source_dijkstra_vertices(MinimalPath.cn1,-6410414390854871141, DistanceType.FOREMOST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {-4790071369877151138: datetime.timedelta(0)}
        self.assertEqual(result, expected_res)

    def test_10(self):
        result = single_source_dijkstra_hyperedges(MinimalPath.cn1,-6410414390854871141, DistanceType.FOREMOST, datetime.datetime(2020,2,5,12,49,39))
        expected_res = {-4790071369877151138: datetime.timedelta(0)}
        self.assertEqual(result, expected_res)

    