#!/bin/bash
set -e

THIS_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Move to the test directory and start the test
cd "${THIS_SCRIPT_DIR}/../python/src"
export PYTHONPATH=$(pwd)
cd ../test
python3 -m unittest -v
