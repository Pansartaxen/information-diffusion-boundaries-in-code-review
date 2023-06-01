import unittest
import datetime
from simulation.model import CommunicationNetwork
from simulation.model import EntityNotFound

class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    cn2 = CommunicationNetwork({'1': {100, 3}},{'1': datetime.datetime(2020,2,5,12,49,39)})

    # TimeVaryingHypergraph
    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})

    def test_timings(self):
        self.assertEqual(len(ModelTest.cn.timings()), 3)
        self.assertEqual(ModelTest.cn.timings('h1'), 1)

    def test_unkown_hyperedge(self):
        with self.assertRaises(EntityNotFound):
            ModelTest.cn2.hyperedges(-1)

    def test_unkown_vertices(self):
        with self.assertRaises(EntityNotFound):
            ModelTest.cn2.vertices("-1")


    # CommunicationNetwork
    def test_channels(self):
        self.assertEqual(len(ModelTest.cn.channels()), 3)
        self.assertEqual(ModelTest.cn.channels('v1'), {'h1'})

    def test_participants(self):
        self.assertEqual(len(ModelTest.cn.participants()), 4)
        self.assertEqual(ModelTest.cn.participants('h1'), {'v1', 'v2'})


class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)
        
