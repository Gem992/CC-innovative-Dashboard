"""
Quantum vs Classical Comparison – Agent 5
Run both schedulers and print a side-by-side report.
"""

import time
from classical_scheduler import greedy_schedule, TASKS, SERVERS
from quantum_scheduler import quantum_schedule

FUTURE_USE_CASES = """
╔══════════════════════════════════════════════════════════════════════════╗
║           QUANTUM COMPUTING: FUTURE USE CASES IN CLOUD & IoT            ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  1. LOAD BALANCING                                                       ║
║     QAOA can find near-optimal task distributions across cloud servers   ║
║     in O(√N) vs classical O(N²), critical for burst IoT traffic.         ║
║                                                                          ║
║  2. ANOMALY DETECTION                                                    ║
║     Quantum kernel SVMs can classify sensor anomalies using exponentially ║
║     large Hilbert-space feature maps impossible for classical ML.         ║
║                                                                          ║
║  3. REAL-TIME ROUTE OPTIMISATION                                         ║
║     Quantum annealing (D-Wave) solves graph-cut problems for efficient   ║
║     data routing between IoT edge nodes and cloud regions.               ║
║                                                                          ║
║  4. SECURE COMMUNICATIONS                                                ║
║     QKD (Quantum Key Distribution) provides information-theoretic        ║
║     security for IoT device authentication — unbreakable with any        ║
║     classical computer.                                                  ║
║                                                                          ║
║  STATUS: All above are research-stage (2024–2030 horizon).               ║
║  Current demo uses a statevector simulator, not real quantum hardware.   ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def run_comparison():
    print("\n" + "═" * 70)
    print("  QUANTUM vs CLASSICAL RESOURCE SCHEDULING COMPARISON")
    print("═" * 70)
    print(f"\n  Tasks (CPU units): {TASKS}")
    print(f"  Servers: {SERVERS}\n")

    # ── Classical ──────────────────────────────────────────────────────────
    t0 = time.time()
    c_assign, c_makespan = greedy_schedule()
    c_time_ms = round((time.time() - t0) * 1000, 3)

    c_loads = [0] * SERVERS
    for task_i, srv in enumerate(c_assign):
        c_loads[srv] += sorted(TASKS, reverse=True)[task_i]

    print("┌─── CLASSICAL (LPT Greedy) ──────────────────────────────────┐")
    print(f"│  Makespan (max server load): {c_makespan} CPU units")
    print(f"│  Server loads: {c_loads}")
    print(f"│  Time taken:   {c_time_ms} ms")
    print("└─────────────────────────────────────────────────────────────┘\n")

    # ── Quantum ────────────────────────────────────────────────────────────
    t0 = time.time()
    q_assign, q_makespan, q_detail = quantum_schedule()
    q_time_ms = round((time.time() - t0) * 1000, 3)

    q_loads = [0] * SERVERS
    for task_i, srv in enumerate(q_assign):
        q_loads[srv] += TASKS[task_i]

    print("┌─── QUANTUM (QAOA-style circuit, statevector sim) ───────────┐")
    print(f"│  Makespan (max server load): {q_makespan} CPU units")
    print(f"│  Server loads: {q_loads}")
    print(f"│  Time taken:   {q_time_ms} ms")
    print(f"│  Detail:\n│    {q_detail.replace(chr(10), chr(10) + '│    ')}")
    print("└─────────────────────────────────────────────────────────────┘\n")

    # ── Summary ────────────────────────────────────────────────────────────
    winner = "Quantum" if q_makespan <= c_makespan else "Classical"
    print(f"  🏆  Better makespan: {winner}")
    print(f"  Note: Classical is faster on classical hardware by design.")
    print()
    print(FUTURE_USE_CASES)


if __name__ == "__main__":
    run_comparison()
