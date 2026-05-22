"""
monte_carlo.py — Deliverable 2: Monte Carlo Simulation
UST Sustainability Campus Game

Compares two autonomous navigation strategies over 300 simulated game runs:

  Strategy 1  Nearest Site   — always navigate to the closest uncollected site
  Strategy 2  Best Value     — navigate to the site with the best reward-to-distance ratio
                               (mirrors the A* target-selection logic from the game)

Uncertainty is modeled using real dataset values:
  Travel cost multiplier  — varies by building LEED certification (ust_energy_assets-1.csv)
  Trivia success rate     — stochastic around a 65% baseline informed by UST's 57%
                            waste-diversion rate (ust_sustainability_factors-1.csv)
  Resource effectiveness  — varies with campus sustainability score (51% carbon reduction)

Run:
    cd Final_Project
    python monte_carlo.py
"""

import os
import sys
import heapq
import random

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — safe in all environments
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from models.campus_graph import CampusGraph

# ── Building energy profiles (ust_energy_assets-1.csv) ──────────────────────
# LEED certification tier determines how volatile travel costs are.
# Platinum = most efficient, tightest variation; standard = most volatile.
LEED_PROFILE = {
    "Anderson":    "gold",      # Anderson Student Center  — LEED Gold
    "FreyHall":    "platinum",  # Frey Residence Hall      — LEED Platinum (2020)
    "Schoenecker": "gold",      # Schoenecker Center       — LEED Gold (2024)
}
SOLAR_BUILDINGS = {"Brady"}     # Brady Hall — first campus solar installation (2012)

# ── Campus-wide sustainability baselines (ust_sustainability_factors-1.csv) ─
WASTE_DIVERSION_RATE      = 0.57   # 57 % — proxy for trivia-success floor
CAMPUS_CARBON_REDUCTION   = 0.51   # 51 % carbon reduction since 2007 — scales reward variation

# ── Game constants (kept in sync with SustainabilityGame) ───────────────────
HIGH_PRIORITY_SITES = {
    "GraceHall": 5, "CretinHall": 5, "LorasHall": 5, "FlynnHall": 5,
    "Dowling":   5, "Ireland":    5, "FreyHall":  5, "Anderson":  5,
}
MEDIUM_PRIORITY_SITES = {
    "Library": 3, "Brady": 3, "Murray": 3, "Schoenecker": 3, "McNeely": 3,
}

TRIVIA_BONUS        = 15
TRIVIA_PENALTY      = 5
HIGH_PRIORITY_PTS   = 35
MEDIUM_PRIORITY_PTS = 20
LOW_PRIORITY_PTS    = 10
REVISIT_PENALTY     = 5
DISTANCE_MULT       = 10_000
COMPLETION_BONUS    = 100
MAX_STEPS           = 200       # safety cap: prevents infinite loops

# Simulated player trivia accuracy.
# 65 % — slightly above UST's 57 % waste-diversion rate to account for
# students who chose to play being somewhat sustainability-aware.
BASE_TRIVIA_RATE = 0.65


# ── Stochastic helpers ───────────────────────────────────────────────────────

def get_travel_multiplier(building: str) -> float:
    """
    Return a random travel-cost multiplier for moving INTO `building`.

    Ranges are grounded in ust_energy_assets-1.csv certification tiers:
      LEED Platinum  → 0.80–1.05   (very stable, highly efficient)
      LEED Gold      → 0.85–1.20   (stable)
      Solar-equipped → 0.85–1.20   (partially self-sufficient)
      Standard       → 0.90–1.50   (volatile, demand-driven spikes)
    """
    profile = LEED_PROFILE.get(building)
    if profile == "platinum":
        return random.uniform(0.80, 1.05)
    elif profile == "gold":
        return random.uniform(0.85, 1.20)
    elif building in SOLAR_BUILDINGS:
        return random.uniform(0.85, 1.20)
    else:
        return random.uniform(0.90, 1.50)


def get_resource_effectiveness() -> float:
    """
    Random multiplier on collection reward, representing day-to-day variation
    in how much sustainability impact a collection visit actually delivers.
    Centered at 1.0; spread scaled by the campus carbon-reduction score (0.51).
    """
    spread = CAMPUS_CARBON_REDUCTION * 0.3          # ≈ 0.15
    return random.uniform(1.0 - spread, 1.0 + spread * 0.67)


# ── Game helpers ─────────────────────────────────────────────────────────────

def get_collection_reward(building: str) -> int:
    if building in HIGH_PRIORITY_SITES:
        return HIGH_PRIORITY_PTS
    if building in MEDIUM_PRIORITY_SITES:
        return MEDIUM_PRIORITY_PTS
    return LOW_PRIORITY_PTS


def get_reachable_nodes(graph: CampusGraph, start: str) -> set:
    """BFS to find all nodes reachable from `start` in the campus graph."""
    visited = {start}
    queue   = [start]
    while queue:
        node = queue.pop()
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def build_collection_sites(graph: CampusGraph, reachable: set | None = None) -> dict:
    """
    Return {building: reward} for every collection site in the graph.
    If `reachable` is provided, only include sites reachable from the start building.
    This handles disconnected campus graph components transparently.
    """
    return {
        b: get_collection_reward(b)
        for b in graph.graph
        if (b in HIGH_PRIORITY_SITES or b in MEDIUM_PRIORITY_SITES)
        and (reachable is None or b in reachable)
    }


# ── Pathfinding ──────────────────────────────────────────────────────────────

def dijkstra_path(graph: CampusGraph, start: str, goal: str) -> list:
    """
    Shortest path from `start` to `goal` using base (non-stochastic) edge weights.
    Returns the node list from start (exclusive) to goal (inclusive).
    Stochastic multipliers are applied separately when walking the path.
    """
    if start == goal:
        return []

    dist = {start: 0.0}
    prev: dict = {}
    pq = [(0.0, start)]

    while pq:
        cost, node = heapq.heappop(pq)
        if node == goal:
            break
        if cost > dist.get(node, float("inf")):
            continue
        for neighbor, d in graph.get_neighbors(node):
            nc = cost + d
            if nc < dist.get(neighbor, float("inf")):
                dist[neighbor] = nc
                prev[neighbor] = node
                heapq.heappush(pq, (nc, neighbor))

    if goal not in prev:
        return []   # goal unreachable

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = prev.get(node)
        if node is None:
            return []   # reconstruction failed
    path.reverse()
    return path         # excludes start, includes goal


# ── Strategy target-selection ────────────────────────────────────────────────

def choose_target(strategy: str, current: str, remaining: set,
                  distance_matrix: pd.DataFrame):
    """
    Pick the next collection site to visit.

    nearest    — minimise euclidean distance to target (greedy on distance)
    best_value — maximise (reward − estimated_travel_cost), mirroring the A*
                 target-selection logic used in the live game
    """
    if not remaining:
        return None

    best, best_val = None, float("-inf")

    for site in remaining:
        try:
            d = float(distance_matrix.loc[current, site])
        except (KeyError, ValueError):
            d = float("inf")

        if strategy == "nearest":
            val = -d                                      # minimise distance
        else:
            val = get_collection_reward(site) - d * DISTANCE_MULT

        if val > best_val:
            best_val, best = val, site

    return best


# ── Single simulation run ────────────────────────────────────────────────────

def simulate_run(graph: CampusGraph, distance_matrix: pd.DataFrame,
                 strategy: str, start: str, trivia_rate: float) -> dict:
    """
    Autonomously play one full game and return performance metrics.

    The agent picks a target site using `strategy`, navigates there via the
    shortest graph path (Dijkstra), and applies stochastic costs at each step.
    Trivia outcomes are sampled from a Bernoulli distribution.
    """
    reachable  = get_reachable_nodes(graph, start)
    sites      = build_collection_sites(graph, reachable=reachable)
    remaining  = set(sites)
    collected  = set()
    visited    = {start}
    current    = start
    score      = 0.0
    total_dist = 0.0
    steps      = 0
    t_correct  = 0
    t_total    = 0

    # ── Collect start building if it is a site ───────────────────────────────
    if current in remaining:
        remaining.discard(current)
        collected.add(current)
        score += get_collection_reward(current) * get_resource_effectiveness()
        t_total += 1
        if random.random() < trivia_rate:
            score += TRIVIA_BONUS
            t_correct += 1
        else:
            score -= TRIVIA_PENALTY

    # ── Main navigation loop ─────────────────────────────────────────────────
    while remaining and steps < MAX_STEPS:
        target = choose_target(strategy, current, remaining, distance_matrix)
        if target is None:
            break

        path = dijkstra_path(graph, current, target)
        if not path:
            remaining.discard(target)   # unreachable — skip and try next
            continue

        for building in path:
            steps += 1
            if steps > MAX_STEPS:
                break

            # Find base edge distance
            base_dist = next(
                (d for n, d in graph.get_neighbors(current) if n == building),
                None,
            )
            if base_dist is None:
                current = building
                continue

            # Apply stochastic travel cost (energy-demand volatility)
            actual_dist = base_dist * get_travel_multiplier(building)
            score      -= actual_dist * DISTANCE_MULT
            total_dist += actual_dist

            if building in visited:
                score -= REVISIT_PENALTY

            visited.add(building)
            current = building

            if building in remaining:
                remaining.discard(building)
                collected.add(building)
                score += get_collection_reward(building) * get_resource_effectiveness()
                t_total += 1
                if random.random() < trivia_rate:
                    score += TRIVIA_BONUS
                    t_correct += 1
                else:
                    score -= TRIVIA_PENALTY

    # ── Completion bonus ─────────────────────────────────────────────────────
    completed = not remaining
    if completed:
        score += COMPLETION_BONUS

    return {
        "score":           score,
        "total_distance":  total_dist,
        "sites_collected": len(collected),
        "total_sites":     len(sites),
        "completed":       completed,
        "steps":           steps,
        "trivia_accuracy": t_correct / t_total if t_total else 0.0,
    }


# ── Monte Carlo runner ───────────────────────────────────────────────────────

def run_monte_carlo(graph: CampusGraph, distance_matrix: pd.DataFrame,
                    n_runs: int = 300, start: str = "Anderson") -> dict:
    """Run `n_runs` simulations for each strategy. Returns {label: [run_dicts]}."""
    strategies = {
        "Nearest Site":    "nearest",
        "Best Value (A*)": "best_value",
    }
    results = {}
    for label, key in strategies.items():
        print(f"  '{label}' — {n_runs} runs ...", end=" ", flush=True)
        results[label] = [
            simulate_run(graph, distance_matrix, key, start, BASE_TRIVIA_RATE)
            for _ in range(n_runs)
        ]
        avg = np.mean([r["score"] for r in results[label]])
        print(f"avg score = {avg:.1f}")
    return results


# ── Analysis / reporting ─────────────────────────────────────────────────────

def print_summary(results: dict, n_runs: int) -> None:
    print("\n" + "=" * 66)
    print(f"  MONTE CARLO RESULTS  ({n_runs} runs per strategy)")
    print("=" * 66)
    header = f"{'Strategy':<24} {'Avg':>9} {'Best':>9} {'Worst':>9} {'Std':>8}"
    print(header)
    print("-" * 66)

    for label, runs in results.items():
        scores     = np.array([r["score"] for r in runs])
        dists      = np.array([r["total_distance"] for r in runs])
        sites      = np.array([r["sites_collected"] for r in runs])
        comp_rate  = np.mean([r["completed"] for r in runs]) * 100
        trivia_acc = np.mean([r["trivia_accuracy"] for r in runs]) * 100

        print(f"{label:<24} {scores.mean():>9.1f} {scores.max():>9.1f} "
              f"{scores.min():>9.1f} {scores.std():>8.1f}")
        print(f"  {'Avg distance:':<22} {dists.mean():.5f}")
        print(f"  {'Avg sites collected:':<22} {sites.mean():.1f} / "
              f"{runs[0]['total_sites']}")
        print(f"  {'Completion rate:':<22} {comp_rate:.1f}%")
        print(f"  {'Avg trivia accuracy:':<22} {trivia_acc:.1f}%")
        print()

    print("=" * 66)

    # Narrative analysis
    labels = list(results.keys())
    avgs   = {lb: np.mean([r["score"] for r in results[lb]]) for lb in labels}
    stds   = {lb: np.std([r["score"]  for r in results[lb]]) for lb in labels}
    winner = max(avgs, key=avgs.get)
    stable = min(stds, key=stds.get)

    print("\n  ANALYSIS")
    print(f"  Higher avg score  : {winner}  ({avgs[winner]:.1f})")
    print(f"  More stable (lower std dev): {stable}  (std = {stds[stable]:.1f})")

    if winner == stable:
        print(f"  -> '{winner}' dominates: higher average AND lower variance.")
    else:
        print(f"  -> Trade-off detected:")
        print(f"     '{winner}' scores higher on average but is more variable.")
        print(f"     '{stable}' is safer in worst-case scenarios.")

    comp = {lb: np.mean([r["completed"] for r in results[lb]]) * 100 for lb in labels}
    best_comp = max(comp, key=comp.get)
    print(f"  Completion rate leader: {best_comp}  ({comp[best_comp]:.1f}%)")
    print()


# ── Visualisation ────────────────────────────────────────────────────────────

def plot_results(results: dict, output_dir: str, n_runs: int) -> None:
    os.makedirs(output_dir, exist_ok=True)

    labels  = list(results.keys())
    colors  = ["#27ae60", "#2980b9"]
    palette = dict(zip(labels, colors))

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Monte Carlo Simulation — UST Sustainability Campus Game\n"
        f"({n_runs} runs per strategy | uncertainty modelled from UST energy & "
        f"sustainability datasets)",
        fontsize=12, fontweight="bold",
    )

    # ── 1. Score distribution ────────────────────────────────────────────────
    ax = axes[0, 0]
    for label, runs in results.items():
        scores = [r["score"] for r in runs]
        ax.hist(scores, bins=35, alpha=0.65, label=label,
                color=palette[label], edgecolor="white", linewidth=0.4)
        ax.axvline(np.mean(scores), color=palette[label],
                   linestyle="--", linewidth=1.4)
    ax.set_title("Score Distribution (dashed = mean)")
    ax.set_xlabel("Final Score")
    ax.set_ylabel("Frequency")
    ax.legend()

    # ── 2. Avg / Best / Worst bar chart ─────────────────────────────────────
    ax = axes[0, 1]
    metric_labels = ["Average", "Best Case", "Worst Case"]
    x = np.arange(len(metric_labels))
    w = 0.35
    for i, (label, runs) in enumerate(results.items()):
        scores = [r["score"] for r in runs]
        vals   = [np.mean(scores), np.max(scores), np.min(scores)]
        bars   = ax.bar(x + (i - 0.5) * w, vals, w,
                        label=label, color=palette[label], alpha=0.85)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(abs(v) * 0.01, 1),
                    f"{v:.0f}", ha="center", va="bottom", fontsize=8)
    ax.set_title("Score Statistics Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels)
    ax.set_ylabel("Score")
    ax.legend()

    # ── 3. Total distance distribution ──────────────────────────────────────
    ax = axes[1, 0]
    for label, runs in results.items():
        dists = [r["total_distance"] for r in runs]
        ax.hist(dists, bins=35, alpha=0.65, label=label,
                color=palette[label], edgecolor="white", linewidth=0.4)
        ax.axvline(np.mean(dists), color=palette[label],
                   linestyle="--", linewidth=1.4)
    ax.set_title("Total Distance Traveled (dashed = mean)")
    ax.set_xlabel("Total Distance (campus units, stochastic)")
    ax.set_ylabel("Frequency")
    ax.legend()

    # ── 4. Sites-collected distribution ─────────────────────────────────────
    ax = axes[1, 1]
    all_counts = sorted({r["sites_collected"]
                         for runs in results.values() for r in runs})
    x = np.arange(len(all_counts))
    w = 0.35
    for i, (label, runs) in enumerate(results.items()):
        freq = [sum(1 for r in runs if r["sites_collected"] == c)
                for c in all_counts]
        ax.bar(x + (i - 0.5) * w, freq, w,
               label=label, color=palette[label], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(all_counts)
    ax.set_title("Sites Collected Distribution")
    ax.set_xlabel("Number of Sustainability Sites Collected")
    ax.set_ylabel("Frequency")
    ax.legend()

    plt.tight_layout()
    out_path = os.path.join(output_dir, "monte_carlo_results.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Plot saved -> {out_path}")


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("=" * 66)
    print("  UST Sustainability Game — Monte Carlo Simulation (Deliverable 2)")
    print("=" * 66)

    # Load campus graph
    graph = CampusGraph()
    graph.load_edges(os.path.join(BASE_DIR, "data", "ust_building_edges-1.csv"))

    # Load Euclidean distance matrix (heuristic / strategy guide)
    distance_matrix = pd.read_csv(
        os.path.join(BASE_DIR, "data", "ust_distance_matrix-1.csv"),
        index_col=0,
    )

    # Starting building — Anderson is LEED Gold and a major campus hub
    valid_buildings = list(graph.graph.keys())
    start = "Anderson" if "Anderson" in valid_buildings else valid_buildings[0]

    reachable      = get_reachable_nodes(graph, start)
    all_sites      = build_collection_sites(graph)
    reachable_sites = build_collection_sites(graph, reachable=reachable)

    print(f"\n  Start building     : {start}")
    print(f"  Campus graph nodes : {len(valid_buildings)}")
    print(f"  Collection sites   : {len(reachable_sites)} reachable"
          f" / {len(all_sites)} total")
    if len(reachable_sites) < len(all_sites):
        skipped = set(all_sites) - set(reachable_sites)
        print(f"  (Unreachable sites excluded from sim: {', '.join(sorted(skipped))})")
    print(f"  Trivia success rate: {BASE_TRIVIA_RATE * 100:.0f}% (stochastic)")
    print(f"  Travel cost model  : LEED/Solar-grounded multipliers per edge")
    print(f"  Runs per strategy  : 300\n")

    N = 300
    print("Running Monte Carlo simulation...")
    results = run_monte_carlo(graph, distance_matrix, n_runs=N, start=start)

    print_summary(results, n_runs=N)

    out_dir = os.path.join(BASE_DIR, "monte_carlo_results")
    plot_results(results, out_dir, n_runs=N)


if __name__ == "__main__":
    main()
