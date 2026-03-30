"""
Quantum Resource Scheduler – Agent 5
Demonstrates a QAOA-inspired approach to bin-packing / load-balancing.
Uses Qiskit's statevector simulator so no real quantum hardware is needed.
"""

from __future__ import annotations
import math
import time
from typing import List, Tuple

# ── Graceful import ────────────────────────────────────────────────────────
try:
    from qiskit import QuantumCircuit
    from qiskit.primitives import StatevectorSampler
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("⚠️  Qiskit not installed.  Quantum part will use a stub.")


# ── Problem definition ─────────────────────────────────────────────────────
# We have N cloud servers and M IoT tasks with varying CPU demands.
# Goal: schedule tasks across servers to minimise max-load (makespan).

SERVERS = 3
TASKS: List[int] = [4, 7, 2, 9, 5, 3, 8, 1, 6, 4]   # CPU units each


# ── Quantum scheduler ──────────────────────────────────────────────────────

def _build_qaoa_circuit(n_qubits: int, gamma: float, beta: float) -> "QuantumCircuit":
    """Build a single-layer QAOA-style circuit (illustrative, not exact QAOA)."""
    qc = QuantumCircuit(n_qubits)

    # Initial superposition
    qc.h(range(n_qubits))

    # Problem unitary (phase separation) — encode task cost as RZ rotation
    for i in range(n_qubits):
        qc.rz(gamma * TASKS[i % len(TASKS)], i)

    # Mixer unitary
    for i in range(n_qubits):
        qc.rx(2 * beta, i)

    qc.measure_all()
    return qc


def quantum_schedule() -> Tuple[List[int], float, str]:
    """
    Run a simplified QAOA circuit and interpret the most-frequent bit-string
    as a task-to-server assignment.

    Returns (assignment, makespan, detail_string)
    """
    if not QISKIT_AVAILABLE:
        # Stub fallback
        assignment = [i % SERVERS for i in range(len(TASKS))]
        loads = [0] * SERVERS
        for task_idx, server in enumerate(assignment):
            loads[server] += TASKS[task_idx]
        return assignment, float(max(loads)), "⚠️  Qiskit stub result"

    n_qubits = len(TASKS)
    gamma, beta = 0.5, 0.3

    qc = _build_qaoa_circuit(n_qubits, gamma, beta)

    sampler = StatevectorSampler()
    job = sampler.run([qc], shots=1024)
    result = job.result()
    counts = result[0].data.meas.get_counts()

    # Pick the most-frequent bit-string
    best_bits = max(counts, key=counts.get)
    # Map each bit → server index (mod SERVERS)
    assignment = [int(b) % SERVERS for b in best_bits]

    loads = [0] * SERVERS
    for task_idx, server in enumerate(assignment):
        loads[server] += TASKS[task_idx]

    makespan = max(loads)
    detail = (
        f"Circuit: {n_qubits} qubits | shots=1024\n"
        f"Best bit-string: {best_bits} (count={counts[best_bits]})\n"
        f"Server loads: {loads}"
    )
    return assignment, float(makespan), detail
