import json
import math
import os
import sys
import random
from copy import deepcopy

def calculate_distance(a1, a2):
    # Calculate straight-line distance between two 2D points
    return math.sqrt((a1[0] - a2[0]) ** 2 + (a1[1] - a2[1]) ** 2)

def load_data(filepath):

    with open(filepath, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    raw_wh = raw.get("warehouses", {})
    warehouses = {w["id"]: w["location"] for w in raw_wh} if isinstance(raw_wh, list) else dict(raw_wh)

    raw_ag = raw.get("agents", {})
    agents = {a["id"]: a["location"] for a in raw_ag} if isinstance(raw_ag, list) else dict(raw_ag)

    packages = []
    for pkg in raw.get("packages", []):
        wh_key = pkg.get("warehouse") or pkg.get("warehouse_id")
        packages.append({"id": pkg["id"], "warehouse": wh_key, "destination": pkg["destination"]})

    return {"warehouses": warehouses, "agents": agents, "packages": packages}

def assign_simulate(warehouses, agents, packages, random_delays=False):

    agent_pos = deepcopy(agents)

    stats = {
        aid: {"packages_delivered": 0, "total_distance": 0.0, "delays": []}
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

        # Bonus: random delay simulation (30% probability)
        if random_delays and random.random() < 0.30:
            delay = random.randint(5, 30)
            stats[nearest]["delays"].append({"package": pkg["id"], "delay_minutes": delay})

        agent_pos[nearest] = list(dest)

    for s in stats.values():
        s["total_distance"] = round(s["total_distance"], 2)

    return stats

def ascii_visualise(warehouses, agents, packages):

    WIDTH, HEIGHT = 60, 30

    all_coords = (
        list(warehouses.values()) +
        list(agents.values()) +
        [p["destination"] for p in packages]
    )
    all_x = [c[0] for c in all_coords]
    all_y = [c[1] for c in all_coords]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    x_range = max_x - min_x or 1
    y_range = max_y - min_y or 1

    def to_grid(x, y):
        gx = round((x - min_x) / x_range * (WIDTH - 1))
        gy = round((y - min_y) / y_range * (HEIGHT - 1))
        return gx, HEIGHT - 1 - gy  # flip y: origin at bottom-left

    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for pkg in packages:
        gx, gy = to_grid(*pkg["destination"])
        grid[gy][gx] = "*"

    for loc in warehouses.values():
        gx, gy = to_grid(*loc)
        grid[gy][gx] = "W"

    for loc in agents.values():
        gx, gy = to_grid(*loc)
        grid[gy][gx] = "A"

    print("\n" + "=" * (WIDTH + 4))
    print("  FastBox Route Map  (W=warehouse  A=agent  *=destination)")
    print("=" * (WIDTH + 4))
    for row in grid:
        print("| " + "".join(row) + " |")
    print("=" * (WIDTH + 4) + "\n")

def compute_efficiency(stats):
    for s in stats.values():
        s["efficiency"] = (
            round(s["total_distance"] / s["packages_delivered"], 2)
            if s["packages_delivered"] > 0 else None
        )
    return stats

def find_best_agent(stats):
    eligible = {aid: s for aid, s in stats.items() if s["efficiency"] is not None}
    return min(eligible, key=lambda aid: (eligible[aid]["efficiency"], aid)) if eligible else None

def build_report(stats, best_agent):
    report = {}
    for aid, s in stats.items():
        report[aid] = {
            "packages_delivered": s["packages_delivered"],
            "total_distance": s["total_distance"],
            "efficiency": s["efficiency"],
        }
        if s["delays"]:
            report[aid]["delays"] = s["delays"]
    report["best_agent"] = best_agent
    return report

def save_report(report, output_path):
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"[✓] Report saved -> {output_path}")

def main():
    filepath = "base_case.json"
    output = "report.json"
    use_delays = False   # set True to enable bonus delays
    show_map = True      # set True to show ASCII map

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = load_data(filepath)
    warehouses, agents, packages = data["warehouses"], data["agents"], data["packages"]

    print(f"[i] Loaded {len(warehouses)} warehouses, {len(agents)} agents, {len(packages)} packages.")

    if show_map:
        ascii_visualise(warehouses, agents, packages)

    stats = assign_simulate(warehouses, agents, packages, use_delays)
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
