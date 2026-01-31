import pytest
import sys
import os
from unittest.mock import MagicMock

# Add python-brain to path
sys.path.insert(0, os.path.join(os.getcwd(), 'agents', 'python-brain'))

from core.autonomous_controller import AutonomousController

class TestAutonomousController:
    @pytest.fixture
    def controller(self):
        memory = MagicMock()
        learning = MagicMock()
        
        # Mock learning recommendation
        learning.get_recommended_strategy.return_value = {
            "confidence": 0.8,
            "recommended_techniques": [{"technique": "Mocked Tech"}]
        }
        
        ctrl = AutonomousController(memory, learning)
        return ctrl

    def test_suggest_from_memory(self, controller):
        suggestion = controller.suggest_next_action("State...", "Goal...")
        assert "Mocked Tech" in suggestion

    def test_health_check_warnings(self, controller):
        result = {"status": "failed"}
        warnings = controller.check_health(result)
        assert len(warnings) > 0
        assert "Last action failed" in warnings[0]

    def test_max_consecutive_limit(self, controller):
        controller.max_consecutive = 1
        controller.consecutive_count = 1
        
        suggestion = controller.suggest_next_action("State", "Goal")
        assert suggestion is None
