# FastBox Delivery System Simulator

A logistics simulator for a fictional delivery company **FastBox**.  
Simulates one day of operations — assigns packages to agents, calculates distances, and generates a performance report.

---

## Project Structure

delivery_system/
├── delivery_system.py       # Main simulator
├── run_tests.py             # Batch test runner
├── base_case.json           # Base input data
├── report.json              # Generated report (after running)
├── test_cases/
│   ├── test_case_1.json
│   ├── test_case_2.json
│   └── ... test_case_10.json
└── test_outputs/            # Reports for all test cases (after running)

---

## Requirements

- Python 3.8+
- No external libraries required (uses standard library only)

---

## How to Run

### Basic run (base case)

python delivery_system.py data.json


### Run a specific test case

python delivery_system.py test_cases/test_case_1.json


### Run all test cases at once

python run_tests.py

### All bonuses together

python delivery_system.py data.json --visualise --delays --new-agent "A4,10,20" --csv top.csv


## Output Report Format

```json
{
  "A1": {
    "packages_delivered": 2,
    "total_distance": 85.32,
    "efficiency": 42.66
  },
  "A2": {
    "packages_delivered": 2,
    "total_distance": 120.12,
    "efficiency": 60.06
  },
  "A3": {
    "packages_delivered": 1,
    "total_distance": 50.00,
    "efficiency": 50.00
  },
  "best_agent": "A1"
}
```

- **efficiency** = total_distance / packages_delivered (lower is better)
- **best_agent** = agent with lowest efficiency score

---

## How It Works

1. Loads warehouses, agents, and packages from a JSON file
2. For each package, assigns the **nearest agent** (Euclidean distance from agent to warehouse)
3. Agent travels: current position → warehouse → destination
4. Agent's position updates to the delivery destination after each delivery
5. Efficiency and best agent are calculated from the final stats
