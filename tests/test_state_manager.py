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

if __name__ == '__main__':
    unittest.main()
