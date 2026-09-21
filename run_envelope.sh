#!/bin/bash

set -eo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

MORL_DIR="${MORL_DIR:-$ROOT/morl-baselines-ben}"
TARGET="$MORL_DIR/morl_baselines/multi_policy/envelope/envelope.py"

ENVELOPE_FILE="${ENVELOPE_FILE:-envelope_default.py}"

if [ ! -f "$ROOT/envelope/$ENVELOPE_FILE" ]; then
    echo "Can't find $ROOT/envelope/$ENVELOPE_FILE" >&2
    exit 1
fi


source "$(conda info --base)/etc/profile.d/conda.sh"
echo "Activating the environment: my_env"
conda activate my_env

[ -f "$TARGET.orig" ] || cp "$TARGET" "$TARGET.orig"   # keep a backup once

echo "Replacing the envelope.py with the edited version."
cp "$ROOT/envelope/envelope.py" "$TARGET"

echo "Running file"
python "$ROOT/envelope/$ENVELOPE_FILE"

