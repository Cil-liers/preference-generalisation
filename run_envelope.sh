#!/bin/bash

# conda activate my_env
# python ./envelope/envelope_default.py # File to be run is set to the default

set -eo pipefail

MORL_DIR="./morl-baselines-ben"
TARGET="$MORL_DIR/morl_baselines/multi_policy/envelope/envelope.py"

if [ "$1" = "--restore" ]; then
    if [ ! -f "$TARGET.orig" ]; then
        echo "No backup found, nothing to restore." >&2
        exit 1
    fi
    cp "$TARGET.orig" "$TARGET"
    echo "Restored the origianl envelope.py"
    exit 0
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
echo "Activating the environment: my_env"
conda activate my_env

[ -f "$TARGET.orig" ] || cp "$TARGET" "$TARGET.orig"   # keep a backup once
echo "Replacing the original with the edited version."
cp "./envelope/envelope.py" "$TARGET"

echo "Running file"
python "./envelope/envelope_default.py"
