import sys
if sys.stdin.isatty():
    print("No input provided. Please pipe data into this script.")
    sys.exit(1)
data = [float(x.strip().strip(",") or "nan") for x in sys.stdin];