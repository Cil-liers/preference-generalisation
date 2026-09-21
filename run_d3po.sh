#!/bin/bash


set -eo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

source "$(conda info --base)/etc/profile.d/conda.sh"
echo "Activating conda environment: my_env_d3po"
conda activate my_env_d3po

MAIN_VERSION="${MAIN_VERSION:-main_ppo_default.py}"

if [ ! -f "$ROOT/D3PO/$MAIN_VERSION" ]; then
  echo "Can't find $ROOT/D3PO/$MAIN_VERSION" >&2
  exit 1
fi

RD="$ROOT/reward-decomposition"

echo "Replacing main_ppo.py and ppo.py with edited versions"
for pair in "ppo/ppo.py:ppo.py" "main_ppo.py:$MAIN_VERSION"; do
  dest="${pair%%:*}"
  src="${pair##*:}"

  [ -f "$RD/$dest.orig" ] || cp "$RD/$dest" "$RD/$dest.orig"
  cp "$ROOT/D3PO/$src" "$RD/$dest"
done

export PYTHONPATH="${PYTHONPATH:-}:$ROOT"
EXP_NAME="${1:-d3po_minecart}"        # usage: bash run_d3po.sh my_experiment
USE_WANDB="${USE_WANDB:-False}"       # USE_WANDB=True to enable

echo "Running file"
python "$RD/main_ppo.py" --env_id minecart-v0 --env_is_discrete True \
  --total_timesteps 5000000 --entropy_loss_coefficient 0.05 \
  --use_wandb "$USE_WANDB" --use_tensorboard False \
  --algo "$EXP_NAME" --save_model False --seed 0
