#!/bin/sh

set -ex

###########################
###########################
# Installs

npm i
npm i --save-dev @types/httptoolkit__esm

###########################
###########################
# Linters

# Python
./scripts/lint.sh

# CDK
npm run lint

###########################
###########################
# Tests

# Python
source venv/bin/activate
python -m pytest -v test_python/

# CDK
# TODO: This test fails with an import error.
# npm run test

###########################
###########################
# Deploy

cdk deploy --all --require-approval never --concurrency 5
