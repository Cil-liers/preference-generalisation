#!/bin/bash

# seed is set to 0 by default
# Change the name of experiment to your specific one

conda activate my_env_d3po
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python ./reward-decomposition/main_ppo.py --env_id minecart-v0 --env_is_discrete True --total_timesteps 5000000 --entropy_loss_coefficient 0.05 --use_wandb True --use_tensorboard False --algo "name_of_experiment" --save_model False --seed 0
