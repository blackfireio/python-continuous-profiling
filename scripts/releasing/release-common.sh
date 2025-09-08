#!/bin/bash

set -eu

# a TWINE_PASSWORD environment varialbe is required for it to work.
function release()
{
    wheel_path="$1"

    twine upload $wheel_path/*.whl --verbose
}
