import unittest
import os
import shutil
from orchestrator.state_manager import StateManager

class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/tmp/stingbot_test_state"
        os.makedirs(self.test_dir, exist_ok=True)
        self.state = StateManager(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_node(self):
        res = self.state.add_node("192.168.1.1", "asset", {"os": "Linux"})
        self.assertTrue(res)
        self.assertEqual(len(self.state.graph["nodes"]), 1)
        
        # Duplicate node
        res_dup = self.state.add_node("192.168.1.1", "asset")
        self.assertFalse(res_dup)

    def test_add_edge(self):
        self.state.add_node("192.168.1.1", "asset")
        self.state.add_node("port_80", "vuln")
        self.state.add_edge("192.168.1.1", "port_80", "scan", "success")
        
        self.assertEqual(len(self.state.graph["edges"]), 1)
        self.assertEqual(self.state.graph["edges"][0]["source"], "192.168.1.1")

    def test_memory(self):
        self.state.update_memory("current_target", "10.0.0.5")
        self.assertEqual(self.state.get_memory("current_target"), "10.0.0.5")

    def test_graph_export(self):
        # Add some data to graph
        self.state.add_node("target1", "asset", {"ip": "192.168.1.1"})
        self.state.add_node("vuln1", "vulnerability", {"type": "SQL Injection"})
        self.state.add_edge("target1", "vuln1", "scan", "found")
        
        # Export summary
        summary = self.state.export_summary()
        self.assertIsNotNone(summary)
        self.assertIsInstance(summary, dict)

    def test_multiple_edges(self):
        # Test multiple edges between nodes
        self.state.add_node("node1", "asset")
        self.state.add_node("node2", "asset")
        
        self.state.add_edge("node1", "node2", "scan", "success")
        self.state.add_edge("node1", "node2", "exploit", "failed")
        
        self.assertEqual(len(self.state.graph["edges"]), 2)

if __name__ == '__main__':
    unittest.main()
