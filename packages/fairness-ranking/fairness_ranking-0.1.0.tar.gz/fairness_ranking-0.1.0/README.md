# Fairness Ranking

This package provides functions for generating synthetic data, reranking students based on tolerance, and calculating fairness metrics.

## Installation

To install the package from PyPI, run:

```bash
pip install fairness_ranking



Usage
Here is an example of how to use the package:



import fairness_ranking.ranking as fr

# Define the number of candidates and tolerance
num_candidates = 10
tolerance = 252

# Generate synthetic data
synthetic_data = fr.generate_synthetic_data(num_candidates, 'A vs B')

# Rerank the synthetic data
reranked_data = fr.rerank_students(synthetic_data, tolerance)

# Calculate rewards and totals
data_with_rewards, total_w, total_b = fr.add_rewards_and_calculate_totals(reranked_data, 'linear')

# Calculate fairness metric
initial_rewards = {'w': total_w, 'b': total_b}
post_reranking_rewards = {'w': total_w, 'b': total_b}
fairness_metric = fr.calculate_fairness_metric(initial_rewards, post_reranking_rewards)

print(f"Fairness Metric: {fairness_metric}")



Functions
generate_synthetic_data(num_candidates, gap_scenario, seed=42)
Generates synthetic data with varying gaps between candidate scores.

num_candidates: Number of candidates.
gap_scenario: The scenario defining the score gaps ('A vs B', 'A vs C', 'A vs D', 'MIX').
seed: Seed for random number generation (default is 42).
rerank_students(students, tolerance)
Reranks students based on a given tolerance.

students: List of student dictionaries with scores and groups.
tolerance: Tolerance value for reranking.
calculate_logarithmic_rewards(n)
Calculates logarithmic rewards.

n: Number of candidates.
add_rewards_and_calculate_totals(data, reward_type='linear')
Adds rewards to the data and calculates total rewards for each group.

data: List of candidate dictionaries with scores and groups.
reward_type: Type of rewards ('linear' or 'logarithmic').
calculate_fairness_metric(initial_rewards, post_reranking_rewards)
Calculates the fairness metric based on initial and post-reranking rewards.

initial_rewards: Dictionary with initial total rewards for each group.
post_reranking_rewards: Dictionary with post-reranking total rewards for each group.


