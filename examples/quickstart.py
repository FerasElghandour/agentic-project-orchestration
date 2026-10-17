"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

from dataclasses import asdict
from orchestration import Review, revise
# Deterministic callbacks demonstrate a bounded revision, not an LLM evaluation.
def worker(prompt):
    return 'ready' if 'Required correction:' in prompt else 'draft'
result = asdict(revise('Return ready', worker, lambda response: Review(response == 'ready', 'Return ready')))

import json
print(json.dumps(result, indent=2))

