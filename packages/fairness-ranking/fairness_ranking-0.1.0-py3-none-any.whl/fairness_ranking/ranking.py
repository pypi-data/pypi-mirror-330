import pandas as pd
import random
import locale

# Set the locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def generate_synthetic_data(num_candidates, gap_scenario, seed=42):
    random.seed(seed)  # Set the seed for reproducibility
    data = []

    if gap_scenario == 'A vs B':
        scores_a = sorted(random.sample(range(750, 1001), num_candidates // 2), reverse=True)
        scores_b = sorted(random.sample(range(500, 750), num_candidates // 2), reverse=True)
    elif gap_scenario == 'A vs C':
        scores_a = sorted(random.sample(range(750, 1001), num_candidates // 2), reverse=True)
        scores_c = sorted(random.sample(range(250, 500), num_candidates // 2), reverse=True)
    elif gap_scenario == 'A vs D':
        scores_a = sorted(random.sample(range(750, 1001), num_candidates // 2), reverse=True)
        scores_d = sorted(random.sample(range(0, 250), num_candidates // 2), reverse=True)
    elif gap_scenario == 'MIX':
        scores = sorted(random.sample(range(100, 1001), num_candidates), reverse=True)
        for i in range(num_candidates):
            candidate_id = f"candidate{i+1}"
            group = 'w' if i % 2 == 0 else 'b'
            score = scores[i]
            data.append({"candidate": candidate_id, "score": score, "group": group})
        return data

    for i in range(num_candidates):
        candidate_id = f"candidate{i+1}"
        if i < num_candidates // 2:
            group = 'w'
            score = scores_a[i]
        else:
            group = 'b'
            if gap_scenario == 'A vs B':
                score = scores_b[i - num_candidates // 2]
            elif gap_scenario == 'A vs C':
                score = scores_c[i - num_candidates // 2]
            elif gap_scenario == 'A vs D':
                score = scores_d[i - num_candidates // 2]
        data.append({"candidate": candidate_id, "score": score, "group": group})

    return data

def rerank_students(students, tolerance):
    students_sorted = sorted(students, key=lambda x: x["score"], reverse=True)
    reranked_students = []

    for current in students_sorted:
        placed = False
        for i in range(len(reranked_students)):
            existing = reranked_students[i]
            if current["group"] == 'b' and existing["group"] == 'w':
                if current["score"] + tolerance >= existing["score"]:
                    reranked_students.insert(i, current)
                    placed = True
                    break
        if not placed:
            reranked_students.append(current)

    return reranked_students

def calculate_logarithmic_rewards(n):
    return [10000 / (1 + i) for i in range(n)]

def add_rewards_and_calculate_totals(data, reward_type='linear'):
    total_candidates = len(data)

    if reward_type == 'linear':
        rewards = list(range(1000, 1000 - total_candidates * 10, -10))
    elif reward_type == 'logarithmic':
        rewards = calculate_logarithmic_rewards(total_candidates)
    else:
        raise ValueError("Invalid reward type. Use 'linear' or 'logarithmic'.")

    # Assign rewards in the order of the current data list
    for i, candidate in enumerate(data):
        candidate['reward'] = rewards[i]

    df = pd.DataFrame(data)
    total_rewards_w = df[df['group'] == 'w']['reward'].sum()
    total_rewards_b = df[df['group'] == 'b']['reward'].sum()
    return data, total_rewards_w, total_rewards_b

def calculate_fairness_metric(initial_rewards, post_reranking_rewards):
    initial_white_rewards = initial_rewards['w']
    initial_black_rewards = initial_rewards['b']
    post_white_rewards = post_reranking_rewards['w']
    post_black_rewards = post_reranking_rewards['b']

    initial_diff = initial_white_rewards - initial_black_rewards
    post_diff = post_white_rewards - post_black_rewards

    if initial_diff == 0:
        return 1.0 if post_diff == 0 else 0.0

    if initial_diff > 0:
        fairness_metric = abs(post_diff - initial_diff) / initial_diff
    else:
        fairness_metric = abs(post_diff - initial_diff) / max(abs(initial_diff), 1)

    return min(1.0, fairness_metric)
