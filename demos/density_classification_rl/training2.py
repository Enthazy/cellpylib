import numpy as np

import cellpylib as cpl
from demos.density_classification_rl.classification_policy import ClassificationPolicy


n_input = 149
n_ca_timesteps = 149
n_episodes = 100000
n_output = 128
n_hidden = 500
learning_rate = 0.5
n_trials = 10

policy = ClassificationPolicy(n_input=n_input, n_hidden=n_hidden, n_output=n_output)

for episode_num in range(1, n_episodes + 1):
    noise = cpl.init_random(n_input)

    # ideal_rule = 6667021275756174439087127638698866559
    # rule_bits = policy.sample(noise) if episode_num % 2 == 0 else cpl.int_to_bits(ideal_rule, n_output)

    rule_bits = policy.sample(noise)

    rule_number = cpl.bits_to_int(rule_bits)

    rewards = []
    for trial in range(n_trials):
        state = cpl.init_random(n_input)
        density_of_1s = np.count_nonzero(state) / n_input

        ca = cpl.evolve(state, timesteps=n_ca_timesteps,
                        apply_rule=lambda n, c, t: cpl.binary_rule(n, rule_number), r=3)
        final_state = ca[-1]

        reward = 0
        if density_of_1s > 0.5 and np.count_nonzero(final_state) == n_input:
            reward = 1
        if density_of_1s < 0.5 and np.count_nonzero(final_state) == 0:
            reward = 1
        rewards.append(reward)

    total_reward = np.sum(rewards)

    policy.update(noise, total_reward, rule_bits, learning_rate)

    print("episode: %s; rule #: %s; total reward: %s" % (episode_num, rule_number, total_reward))