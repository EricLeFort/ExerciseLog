#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export PYTHONPATH="${SCRIPT_DIR}/../src/"
python3 "${SCRIPT_DIR}/../src/exercise_log/update_visuals.py"
