# Agent 5 — Quantum Module

## Overview
Demonstrates a QAOA-style quantum circuit for IoT workload scheduling on cloud servers, compared against a classical greedy baseline.

## Components
| File | Purpose |
|---|---|
| `quantum_scheduler.py` | QAOA-style Qiskit circuit for task scheduling |
| `classical_scheduler.py` | Classical LPT greedy scheduler |
| `compare.py` | Side-by-side comparison runner |

## Setup & Run

```bash
cd quantum
pip install -r requirements.txt

# Run the comparison
python compare.py
```

> If Qiskit is not installed, the quantum scheduler uses a deterministic stub so you can still see the comparison output.

## Output
```
══════════════════════════════════════════════
  QUANTUM vs CLASSICAL RESOURCE SCHEDULING
══════════════════════════════════════════════

Tasks: [4, 7, 2, 9, 5, 3, 8, 1, 6, 4]  |  Servers: 3

CLASSICAL (LPT Greedy)
  Makespan: 17 CPU units
  Server loads: [17, 15, 17]

QUANTUM (QAOA-style, statevector sim)
  Makespan: XX CPU units
  ...
```

## Future Use Cases in Cloud Load Balancing
1. **Optimal task scheduling** — QAOA finds near-optimal bin-packing solutions exponentially faster than brute force for large N.
2. **Anomaly-aware routing** — Quantum amplitude estimation can detect burst traffic patterns.
3. **QKD security** — Quantum Key Distribution for IoT device authentication.
