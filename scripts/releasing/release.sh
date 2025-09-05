#!/bin/bash

set -eu

SCRIPT_HOME="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

source "$SCRIPT_HOME/release-common.sh"

wheel_path="$1"

release $wheel_path
