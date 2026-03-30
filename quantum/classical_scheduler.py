"""
Classical Greedy Scheduler – Agent 5
Used as the baseline comparison against the quantum scheduler.
"""

from typing import List, Tuple

SERVERS = 3
TASKS: List[int] = [4, 7, 2, 9, 5, 3, 8, 1, 6, 4]   # CPU units (must match quantum_scheduler.py)


def greedy_schedule(tasks: List[int] = TASKS, n_servers: int = SERVERS) -> Tuple[List[int], float]:
    """
    Longest-Processing-Time (LPT) greedy scheduling.
    Assigns each task (in descending order) to the currently least-loaded server.
    Returns (assignment list, makespan).
    """
    loads = [0] * n_servers
    assignment = []

    for task in sorted(tasks, reverse=True):
        # Pick server with minimum current load
        server = loads.index(min(loads))
        loads[server] += task
        assignment.append(server)

    return assignment, float(max(loads))
