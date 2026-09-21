import mo_gymnasium as mo_gym
import numpy as np
from mo_gymnasium.wrappers import MORecordEpisodeStatistics

from morl_baselines.multi_policy.envelope.envelope import Envelope
from morl_baselines.common.weights import equally_spaced_weights




def generate_difficult_weights(n):
        
    num_eval_weights = 100
    num_train_weights = n 

    total = num_eval_weights + num_train_weights
    pts = np.array(equally_spaced_weights(dim=3, n=total))

    column = pts[:, 0]
    sorted_vals = np.sort(column)[::-1]
    threshold = (sorted_vals[num_train_weights - 1] + sorted_vals[num_train_weights]) / 2
    
    # For training weights in the left corner set idx to 0
    # For training weights in the right corner set idx to 1
    # For training weights in the top corner set idx to 2

    idx = 0
    corner = pts[:, idx] > threshold

    return pts[corner], pts[~corner]


	

def main():
    def make_env():
        env = mo_gym.make("minecart-v0")
        env = MORecordEpisodeStatistics(env, gamma=0.98)
        # env = mo_gym.LinearReward(env)
        return env

    env = make_env()
    eval_env = make_env()
    # RecordVideo(make_env(), "videos/minecart/", episode_trigger=lambda e: e % 1000 == 0)
    # TODO: In order for the code to run properly one must replace the n=0 with n=10, n=20 or n=30 to change the number of training weights.
    # Example:
    # train_weights, eval_weights = generate_difficult_weights(n=10)
    # The above code creates an experiment that provides the agent with 10 training weights.

    train_weights, eval_weights = generate_difficult_weights(n=0)


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
