import json
import os
from datetime import datetime

class StateManager:
    """Manages the attack graph and short-term memory (volatile state)."""
    
    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.graph = {
            "nodes": [], # {id: "ip/domain/user", type: "asset/vuln", data: {}}
            "edges": [], # {from: id, to: id, action: "scan/exploit", result: "success/fail"}
            "metadata": {
                "start_time": datetime.now().isoformat(),
                "status": "active"
            }
        }
        self.memory = {} # Key-value for quick lookups (e.g., "target_ip": "10.0.0.1")
        self.log_path = os.path.join(workspace_path, "logs", "attack_graph.json")

    def add_node(self, node_id, node_type, data=None):
        if not any(n['id'] == node_id for n in self.graph['nodes']):
            self.graph['nodes'].append({
                "id": node_id,
                "type": node_type,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            })
            self._save()
            return True
        return False

    def add_edge(self, source, target, action, result="unknown"):
        self.graph['edges'].append({
            "source": source,
            "target": target,
            "action": action,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def update_memory(self, key, value):
        self.memory[key] = value
        self._save()

    def get_memory(self, key, default=None):
        return self.memory.get(key, default)

    def _save(self):
        """Persist state to disk for recovery/review."""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "w") as f:
            json.dump({
                "graph": self.graph,
                "memory": self.memory
            }, f, indent=4)

    def export_summary(self):
        """Clean summary for context inclusion."""
        nodes = [f"{n['id']} ({n['type']})" for n in self.graph['nodes']]
        edges = [f"{e['source']} -> {e['target']} via {e['action']} ({e['result']})" for e in self.graph['edges']]
        return {
            "discovered_assets": nodes,
            "actions_taken": edges,
            "active_variables": self.memory
        }
