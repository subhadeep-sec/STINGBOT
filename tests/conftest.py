import sys
import os

# Add project root and python-brain to path for all tests
project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
python_brain_path = os.path.join(parent_dir, "agents", "python-brain")

sys.path.insert(0, parent_dir)
sys.path.insert(0, python_brain_path)
