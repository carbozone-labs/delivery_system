import json
import math
import os
import sys

def calculate_distance(a1, a2):
    # Calculate straight-line distance between two 2D points
    return math.sqrt((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2)

def load_data(filepath):
    # Read and parse the JSON file manually
    with open(filepath, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    warehouses = raw.get("warehouses", {})
    agents = raw.get("agents", {})
    packages = raw.get("packages", [])

    return {"warehouses": warehouses, "agents": agents, "packages": packages}

def main():
    # Entry point - load data and print basic info
    filepath = "base_case.json"

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = load_data(filepath)
    print(f"Loaded {len(data['warehouses'])} warehouses")
    print(f"Loaded {len(data['agents'])} agents")
    print(f"Loaded {len(data['packages'])} packages")

if __name__ == "__main__":
    main()