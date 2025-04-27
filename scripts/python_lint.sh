#!/usr/bin/env bash

set -ex

echo "Running black..."
python3 -m black src
python3 -m black test_python

echo "Running isort..."
python3 -m isort src
python3 -m isort test_python

echo "Running flake8..."
python3 -m flake8 --show-source --statistics --config=setup.cfg src
python3 -m flake8 --show-source --statistics --config=setup.cfg test_python

echo "Running mypy..."
mypy src
mypy test_python
