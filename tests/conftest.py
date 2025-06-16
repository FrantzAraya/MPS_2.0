import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# Use in-memory database for tests to avoid persistent state
os.environ.setdefault("DB_URL", ":memory:")
