#!/bin/bash

set -eu

source scripts/release-common.sh

buildkite-agent artifact download 'wheel_dist/manylinux/*' /src

release /src/wheel_dist/manylinux
