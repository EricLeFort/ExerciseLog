#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the test directory and start the test
cd "${SCRIPT_DIR}/../python/test/"
export PYTHONPATH="${SCRIPT_DIR}/../python/src/"
python3 -m unittest
