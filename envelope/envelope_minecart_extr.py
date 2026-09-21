import mo_gymnasium as mo_gym
import numpy as np
from mo_gymnasium.wrappers import MORecordEpisodeStatistics
from morl_baselines.multi_policy.envelope.envelope import Envelope
from morl_baselines.common.weights import equally_spaced_weights
from data.get_easy_extrapolation_weights import get_ex_weights


def get_eval_weights():
    temp = (np.array(equally_spaced_weights(dim=3, n=100))).tolist()
    weights_10 = (np.array(equally_spaced_weights(dim=3, n=10))).tolist()
    weights_20 = (np.array(equally_spaced_weights(dim=3, n=20))).tolist()
    weights_30 = (np.array(equally_spaced_weights(dim=3, n=30))).tolist()

    result = []
    for row in temp:
        if row not in weights_10 and row not in weights_20 and row not in weights_30:
            result.append(row)
    
    return result


	

def main():
    def make_env():
        env = mo_gym.make("minecart-v0")
        env = MORecordEpisodeStatistics(env, gamma=0.98)
        # env = mo_gym.LinearReward(env)
        return env

    env = make_env()
    eval_env = make_env()
    # RecordVideo(make_env(), "videos/minecart/", episode_trigger=lambda e: e % 1000 == 0)
    
    #TODO: In order for the code to run one must replace file_one.txt with an actual training weights file.
    # Example:  
    # train_weights = np.array(get_ex_weights("easy_extrapolation_train_weights_10.txt"))
    # Above depicts an experiment providing the agent with 10 training weights.
    # The the training weight files for extrapolation (Easy) are stored in the data directory.

    train_weights = np.array(get_ex_weights("file_one.txt"))
    eval_weights = np.array(get_ex_weights("easy_extrapolation_evaluation_weights.txt"))



    agent = Envelope(
        env,
        max_grad_norm=0.1,
        learning_rate=3e-4,
        gamma=0.98,
        batch_size=64,
        net_arch=[256, 256, 256, 256],
        buffer_size=int(2e6),
        initial_epsilon=1.0,
        final_epsilon=0.05,
        epsilon_decay_steps=50000,
        initial_homotopy_lambda=0.0,
        final_homotopy_lambda=1.0,
        homotopy_decay_steps=10000,
        learning_starts=100,
        envelope=True,
        gradient_updates=1,
        target_net_update_freq=1000,  # 1000,  # 500 reduce by gradient updates
        tau=1,
        log=False,
        project_name="MORL-Baselines",
        experiment_name="",
        seed=0,
    )

    agent.train(
        total_timesteps=1000000,
        total_episodes=None,
        train_weights=train_weights,
        eval_weights=eval_weights,
        eval_env=eval_env,
        ref_point=np.array([-1, -1, -200.0]),
        known_pareto_front=env.unwrapped.pareto_front(gamma=0.98),
        num_eval_weights_for_front=100,
        eval_freq=1000,
        reset_num_timesteps=False,
        reset_learning_starts=False,
    )


if __name__ == "__main__":
    main()
