"""casework-ui: firm-facing UI over the frozen casework core.

Importing this package wires the sibling casework project onto
sys.path so its modules import as `app`. casework is FROZEN from
this project (goal.md): consume its modules, never modify them.
"""

import sys
from pathlib import Path

# APPEND, not insert: casework-ui's own packages (verify/) must win
# name lookups; casework's root only needs to be reachable for `app`.
CASEWORK = Path(__file__).resolve().parent.parent.parent / "casework"
if str(CASEWORK) not in sys.path:
    sys.path.append(str(CASEWORK))
