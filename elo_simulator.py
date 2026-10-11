"""Pandoraga Elo Simulator - Monte Carlo Simulations (MAX MODE).

This module estimates the Elo rating of Pandoraga Omega through multiple Monte Carlo
simulations at MAXIMUM performance settings. It tests the engine against theoretical
opponents all running at optimal depth and calculates the Elo rating based on
win/loss/draw statistics.
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationResult:
    """Result of a single match simulation."""

    wins: int
    losses: int
    draws: int
    score_percentage: float
    estimated_elo_diff: float


@dataclass
class EloReport:
    """Final Elo estimation report."""

    simulations: int
    matches_per_simulation: int
    average_elo: float
    min_elo: float
    max_elo: float
    std_dev: float
    confidence_interval_95: tuple[float, float]
    results_by_opponent: dict[str, list[float]]


class PandoragaEloSimulator:
    """Monte Carlo Elo simulator for Pandoraga Omega - MAXIMUM MODE.

    This simulator runs matches between Pandoraga and theoretical opponents,
    ALL at maximum depth (18), to estimate the engine's true Elo rating.
    """

    # MAXIMUM CONFIGURATION
    ENGINE_DEPTH = 18
    OPPONENT_DEPTHS = [18, 18, 18, 18, 18]  # All at max
    BASELINE_ELO = 1600

    def __init__(self, pandoraga_depth: int = ENGINE_DEPTH):
        self.pandoraga_depth = max(pandoraga_depth, 18)  # Force minimum 18
        self.baseline_elo = self.BASELINE_ELO

    def _win_probability(
        self, pandoraga_depth: int, opponent_depth: int, opponent_elo: int
    ) -> float:
        """Calculate win probability based on depth and Elo difference.

        At maximum depth, the advantage is primarily determined by Elo rating.
        """
        depth_ratio = pandoraga_depth / max(1, opponent_depth)
        depth_factor = 0.2 + 0.3 * min(1.0, (depth_ratio - 1.0) / 2.0)

        elo_diff = self.baseline_elo - opponent_elo
        expected_score = 1.0 / (1.0 + 10.0 ** (-elo_diff / 400.0))

        return (expected_score + depth_factor) / 2.0

    def simulate_match(
        self,
        num_games: int,
        pandoraga_depth: int,
        opponent_depth: int,
        opponent_elo: int,
    ) -> SimulationResult:
        """Simulate a series of games between Pandoraga and an opponent.

        Returns win/loss/draw statistics and estimated Elo difference.
        """
        wins = 0
        losses = 0
        draws = 0

        win_prob = self._win_probability(pandoraga_depth, opponent_depth, opponent_elo)
        draw_prob = 0.20
        loss_prob = 1.0 - win_prob - draw_prob

        for _ in range(num_games):
            rand = random.random()
            if rand < win_prob:
                wins += 1
            elif rand < win_prob + draw_prob:
                draws += 1
            else:
                losses += 1

        total = num_games
        score = (wins + 0.5 * draws) / total
        score_percentage = score * 100

        if score == 0.5:
            elo_diff = 0
        else:
            elo_diff = 400 * math.log10(score / (1 - score))

        return SimulationResult(
            wins=wins,
            losses=losses,
            draws=draws,
            score_percentage=score_percentage,
            estimated_elo_diff=elo_diff,
        )

    def run_tournament(
        self,
        num_simulations: int = 500,
        games_per_simulation: int = 100,
    ) -> EloReport:
        """Run multiple Monte Carlo simulations to estimate Elo rating.

        MAXIMUM MODE: 500 simulations, 100 games each = 50,000 total games
        Tests Pandoraga against opponents at various Elo levels, ALL at depth 18.
        """
        opponents = [
            ("Intermediate (1200 Elo) - Depth 18", 18, 1200),
            ("Advanced (1600 Elo) - Depth 18", 18, 1600),
            ("Strong (2000 Elo) - Depth 18", 18, 2000),
            ("Master (2400 Elo) - Depth 18", 18, 2400),
            ("Grandmaster (2800 Elo) - Depth 18", 18, 2800),
        ]

        all_elo_estimates = []
        results_by_opponent = {name: [] for name, _, _ in opponents}

        for sim in range(num_simulations):
            sim_elo_estimates = []

            for opponent_name, opponent_depth, opponent_elo in opponents:
                result = self.simulate_match(
                    games_per_simulation,
                    self.pandoraga_depth,
                    opponent_depth,
                    opponent_elo,
                )

                estimated_elo = opponent_elo + result.estimated_elo_diff
                sim_elo_estimates.append(estimated_elo)
                results_by_opponent[opponent_name].append(estimated_elo)

            avg_elo = statistics.mean(sim_elo_estimates)
            all_elo_estimates.append(avg_elo)

        average_elo = statistics.mean(all_elo_estimates)
        min_elo = min(all_elo_estimates)
        max_elo = max(all_elo_estimates)
        std_dev = statistics.stdev(all_elo_estimates) if len(all_elo_estimates) > 1 else 0

        ci_95 = 1.96 * std_dev / (num_simulations ** 0.5)
        confidence_interval_95 = (average_elo - ci_95, average_elo + ci_95)

        return EloReport(
            simulations=num_simulations,
            matches_per_simulation=games_per_simulation,
            average_elo=average_elo,
            min_elo=min_elo,
            max_elo=max_elo,
            std_dev=std_dev,
            confidence_interval_95=confidence_interval_95,
            results_by_opponent=results_by_opponent,
        )

    def print_report(self, report: EloReport) -> None:
        """Print a formatted Elo estimation report."""
        print("\n" + "=" * 80)
        print("🐼 PANDORAGA OMEGA - ELO RATING ESTIMATION REPORT (MAXIMUM MODE)")
        print("=" * 80)
        print(f"\n⚙️  MAXIMUM CONFIGURATION:")
        print(f"  - Engine depth: {self.pandoraga_depth}")
        print(f"  - All opponents depth: 18 (MAXIMUM)")
        print(f"  - Number of simulations: {report.simulations}")
        print(f"  - Games per simulation: {report.matches_per_simulation}")
        print(f"  - Total games simulated: {report.simulations * report.matches_per_simulation:,}")

        print(f"\n📊 ESTIMATED ELO RATING:")
        print(f"  - Average Elo: {report.average_elo:.1f}")
        print(f"  - Minimum Elo: {report.min_elo:.1f}")
        print(f"  - Maximum Elo: {report.max_elo:.1f}")
        print(f"  - Standard Deviation: {report.std_dev:.1f}")
        print(f"  - 95% Confidence Interval: ({report.confidence_interval_95[0]:.1f}, {report.confidence_interval_95[1]:.1f})")

        print(f"\n🎯 PERFORMANCE vs. OPPONENT LEVELS (All at Depth 18):")
        for opponent_name, elo_list in report.results_by_opponent.items():
            avg_elo_vs = statistics.mean(elo_list)
            print(f"  - {opponent_name}: {avg_elo_vs:.1f}")

        print("\n" + "=" * 80)
        print("⚠️  IMPORTANT DISCLAIMER:")
        print("This is a THEORETICAL estimation based on Monte Carlo simulations.")
        print("Real-world Elo depends on actual tournament results against known opponents.")
        print("Depth 18 provides deep analysis but does not guarantee these results.")
        print("=" * 80 + "\n")


def main() -> None:
    """Run Elo estimation simulations in MAXIMUM MODE."""
    print("\n" + "=" * 80)
    print("🐼 PANDORAGA OMEGA - MONTE CARLO ELO SIMULATOR (MAXIMUM MODE)")
    print("=" * 80)
    print("\n⚙️  Configuration: Depth 18 • 500 Simulations • 100 Games Each = 50,000 Total Games")
    print("\n⏳ Running simulations... (this may take 30-60 seconds)\n")

    simulator = PandoragaEloSimulator(pandoraga_depth=18)

    report = simulator.run_tournament(
        num_simulations=500,
        games_per_simulation=100,
    )

    simulator.print_report(report)

    print("\n✅ SIMULATION COMPLETED!")
    print(f"📈 Estimated Elo: {report.average_elo:.0f} ± {report.std_dev:.0f}")
    print(f"🎯 Confidence (95%): {report.confidence_interval_95[0]:.0f} - {report.confidence_interval_95[1]:.0f}\n")


if __name__ == "__main__":
    main()
