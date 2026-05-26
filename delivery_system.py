import json
import math
import os
import sys
from copy import deepcopy

def calculate_distance(a1, a2):
    # Calculate straight-line distance between two 2D points

    return math.sqrt((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2)

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    warehouses = {
        w["id"]: w["location"]
        for w in raw.get("warehouses", [])
    }

    agents = {
        a["id"]: a["location"]
        for a in raw.get("agents", [])
    }

    packages = [
        {
            "id": p["id"],
            "warehouse": p["warehouse_id"],
            "destination": p["destination"]
        }
        for p in raw.get("packages", [])
    ]

    return {
        "warehouses": warehouses,
        "agents": agents,
        "packages": packages
    }

def assign_simulate(warehouses, agents, packages):

    agent_pos = deepcopy(agents)

    stats = {
        aid: {"packages_delivered": 0, "total_distance": 0.0}
        for aid in agent_pos
    }

    for pkg in packages:
        wh_loc = warehouses[pkg["warehouse"]]
        dest = pkg["destination"]

        nearest = min(
            agent_pos.keys(),
            key=lambda aid: (calculate_distance(agent_pos[aid], wh_loc), aid)
        )

        leg1 = calculate_distance(agent_pos[nearest], wh_loc)
        leg2 = calculate_distance(wh_loc, dest)

        stats[nearest]["total_distance"] += leg1 + leg2
        stats[nearest]["packages_delivered"] += 1
        agent_pos[nearest] = list(dest)

    for s in stats.values():
        s["total_distance"] = round(s["total_distance"], 2)

    return stats

def compute_efficiency(stats):
   
    for s in stats.values():
        if s["packages_delivered"] > 0:
            s["efficiency"] = round(s["total_distance"] / s["packages_delivered"], 2)
        else:
            s["efficiency"] = None
    return stats

def find_best_agent(stats):
    
    eligible = {aid: s for aid, s in stats.items() if s["efficiency"] is not None}
    if not eligible:
        return None
    return min(eligible.keys(), key=lambda aid: (eligible[aid]["efficiency"], aid))

def build_report(stats, best_agent):
    
    report = {}
    for aid, s in stats.items():
        report[aid] = {
            "packages_delivered": s["packages_delivered"],
            "total_distance": s["total_distance"],
            "efficiency": s["efficiency"],
        }
    report["best_agent"] = best_agent
    return report

def save_report(report, output_path):
   
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"[✓] Report saved -> {output_path}")

def main():
    filepath = "base_case.json"
    output = "report.json"

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = load_data(filepath)
    stats = assign_simulate(data["warehouses"], data["agents"], data["packages"])
    stats = compute_efficiency(stats)
    best = find_best_agent(stats)
    report = build_report(stats, best)

    print("\n── Delivery Report ──")
    for aid, info in report.items():
        if aid == "best_agent":
            continue
        eff = f"{info['efficiency']:.2f}" if info["efficiency"] else "N/A"
        print(f"  {aid}: {info['packages_delivered']} pkg(s), dist={info['total_distance']}, eff={eff}")
    print(f"\n  Best agent: {best}")

    save_report(report, output)

if __name__ == "__main__":
    main()