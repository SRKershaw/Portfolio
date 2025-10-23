# backend/tests/diagnostic.py
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
  from backend.main import app
  print("Import success!")
except ImportError as e:
  print(f"Import failed: {e}")