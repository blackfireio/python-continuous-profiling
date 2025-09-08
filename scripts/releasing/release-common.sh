#!/bin/bash

set -eu

# This flag toggles the release destination to testing.pypi.org if set to true
DEPLOY_TESTPYPI=false

# a TWINE_PASSWORD environment varialbe is required for it to work.
function release()
{
    wheel_path="$1"

    if [ "$DEPLOY_TESTPYPI" = true ] ; then
        export TWINE_REPOSITORY_URL="https://test.pypi.org/legacy/"
    fi

    twine upload $wheel_path/*.whl --verbose
}
