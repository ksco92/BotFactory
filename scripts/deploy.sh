#!/bin/sh

set -ex

###########################
###########################
# Installs

npm run clean

###########################
###########################
# Linters

# Python
./scripts/python_lint.sh

# CDK
npm run lint

###########################
###########################
# Tests

# Python
source .venv/bin/activate
PYTHONPATH=./src python -m pytest -v test_python/ --cov=src --cov-report=term --cov-report=html:coverage
mkdir -p documentation/python_coverage
rm -rf documentation/python_coverage
mv coverage documentation/python_coverage

# CDK
npm run test

###########################
###########################
# Deploy

npm run deploy
