from pathlib import Path
import sys

if Path(sys.argv[0]).name == "p2s":
    from .stats import *