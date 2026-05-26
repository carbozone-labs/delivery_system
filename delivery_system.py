import json
import math
import os
import sys
from copy import deepcopy

def calculate_distance(a1, a2):
    # Calculate straight-line distance between two 2D points
    return math.sqrt((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2)

def load_data(filepath):
    # Read and parse the JSON file - handles standard schema
    with open(filepath, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    warehouses = raw.get("warehouses", {})
    agents = raw.get("agents", {})
    packages = raw.get("packages", [])

    return {"warehouses": warehouses, "agents": agents, "packages": packages}

def assign_simulate(warehouses, agents, packages):
   
    agent_pos = deepcopy(agents)

    stats = {
        aid: {"packages_delivered": 0, "total_distance": 0.0}
        for aid in agent_pos
    }

    for pkg in packages:
        wh_loc = warehouses[pkg["warehouse"]]
        dest = pkg["destination"]

        # Find nearest agent (from their CURRENT position - not starting position)
        nearest = min(
            agent_pos.keys(),
            key=lambda aid: (calculate_distance(agent_pos[aid], wh_loc), aid)
        )

        # Leg 1: agent current position -> warehouse
        leg1 = calculate_distance(agent_pos[nearest], wh_loc)
        # Leg 2: warehouse -> delivery destination
        leg2 = calculate_distance(wh_loc, dest)

        stats[nearest]["total_distance"] += leg1 + leg2
        stats[nearest]["packages_delivered"] += 1

        # IMPORTANT: update agent position to destination (the fix)
        agent_pos[nearest] = list(dest)

    # Round distances
    for s in stats.values():
        s["total_distance"] = round(s["total_distance"], 2)

    return stats

def main():
    filepath = "base_case.json"

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = load_data(filepath)
    stats = assign_simulate(
        data["warehouses"], data["agents"], data["packages"]
    )

    print("\n── Delivery Stats ──")
    for aid, s in stats.items():
        print(f"  {aid}: {s['packages_delivered']} packages, distance={s['total_distance']}")

if __name__ == "__main__":
    main()