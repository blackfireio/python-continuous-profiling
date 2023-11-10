#!/bin/bash

set -eu

source scripts/release-common.sh

wheel_path="$1"

release $wheel_path
