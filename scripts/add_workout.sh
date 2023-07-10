#!/bin/bash

if [ $# -eq 0 ] || ! [[ $1 =~ [0-9]{2}-[A-Z]{3}-[0-9]{4} ]]
then
    echo "A date should be passed in as the first argument in the form DD-MMM-YYYY e.g. 01-JAN-2023"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Update visuals
export PYTHONPATH="${SCRIPT_DIR}/../src/"
python3 "${SCRIPT_DIR}/../src/exercise_log/update_visuals.py"

# Add the new commit
git add data img
git commit -m "Added $1 workout"
