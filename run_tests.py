import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from delivery_system import load_data, assign_simulate, compute_efficiency, find_best_agent, build_report

TEST_DIR   = os.path.join(os.path.dirname(__file__), "test_cases")
BASE_CASE  = os.path.join(os.path.dirname(__file__), "base_case.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_outputs")

def run_one(filepath: str, label: str) -> dict:
    data       = load_data(filepath)
    stats      = assign_simulate(
        data["warehouses"], data["agents"], data["packages"]
    )
    stats      = compute_efficiency(stats)   # ← yeh line missing thi
    best_agent = find_best_agent(stats)
    report     = build_report(stats, best_agent)
    return report


def print_report(label: str, report: dict) -> None:
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    for aid, info in report.items():
        if aid == "best_agent":
            continue
        eff = (f"{info['efficiency']:.2f}"
               if info["efficiency"] is not None else "N/A")
        print(f"  {aid:4s} | pkgs={info['packages_delivered']:3d} | "
              f"dist={info['total_distance']:8.2f} | eff={eff}")
    print(f"  🏆 Best: {report['best_agent']}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cases = []

    # Base case
    if os.path.exists(BASE_CASE):
        cases.append(("Base Case", BASE_CASE, "base_case"))

    # Numbered test cases
    if os.path.isdir(TEST_DIR):
        for i in range(1, 11):
            fp = os.path.join(TEST_DIR, f"test_case_{i}.json")
            if os.path.exists(fp):
                cases.append((f"Test Case {i}", fp, f"test_case_{i}"))

    if not cases:
        print("[!] No test files found. Place test_case_N.json in ./test_cases/")
        sys.exit(1)

    print(f"\nRunning {len(cases)} test case(s)…")

    for label, filepath, slug in cases:
        report = run_one(filepath, label)
        print_report(label, report)

        out_path = os.path.join(OUTPUT_DIR, f"report_{slug}.json")
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)

    print(f"\nAll reports saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
