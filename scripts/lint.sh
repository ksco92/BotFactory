#!/bin/sh

set -ex

python3 -m black ./src/
python3 -m black ./test_python/

python3 -B -m isort ./src/ ./test_python/
python3 -m flake8 --config=setup.cfg ./
