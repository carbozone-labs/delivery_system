import json
import math
import os
import sys
from copy import deepcopy

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

def assign_packages(warehouses, agents, packages):
    
    agent_pos = deepcopy(agents)
    assignments = {}  # package_id -> agent_id

    for pkg in packages:
        wh_loc = warehouses[pkg["warehouse"]]

        # Find nearest agent to this warehouse
        nearest = min(
            agent_pos.keys(),
            key=lambda aid: (calculate_distance(agent_pos[aid], wh_loc), aid)
        )

        assignments[pkg["id"]] = nearest
        print(f"Package {pkg['id']} assigned to {nearest}")

    return assignments

def main():
    filepath = "base_case.json"

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = load_data(filepath)
    warehouses = data["warehouses"]
    agents = data["agents"]
    packages = data["packages"]

    print(f"Loaded {len(warehouses)} warehouses, {len(agents)} agents, {len(packages)} packages.")

    assignments = assign_packages(warehouses, agents, packages)
    print("\nAssignments:", assignments)

if __name__ == "__main__":
    main()