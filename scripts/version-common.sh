#!/bin/bash

set -eu

git fetch --tags --force

VERSION=$(git describe --tags --abbrev=0 | cut -d '+' -f1)
REV_COUNT=""
INTERNAL_VERSION=""

# when executing this script with a git tag defined by buildkite, we are releasing to production
if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
    VERSION="$BUILDKITE_TAG"
# when executing this script on the master branch, we are releasing internal versions
elif [[ ${BUILDKITE_BRANCH:-} == "master" || ${APPVEYOR_REPO_BRANCH:-} == "master" ]]; then
    INTERNAL_VERSION="${VERSION}+internal"

    # append short sha to avoid collisions with previous releases
    REV_COUNT=$(git rev-parse --short HEAD)
fi

export PYTHON_CONPROF_INTERNAL_VERSION=${INTERNAL_VERSION}
export PYTHON_CONPROF_INTERNAL_REVCOUNT=${REV_COUNT}
export PYTHON_CONPROF_VERSION=${VERSION}

update_version()
{
# add internal prefix&suffix if on master
if [[ ${PYTHON_CONPROF_INTERNAL_VERSION} != "" ]]; then
    VERSION="${PYTHON_CONPROF_INTERNAL_VERSION}"

    if [[ ${PYTHON_CONPROF_INTERNAL_REVCOUNT} != "" ]]; then
        VERSION="${VERSION}.${PYTHON_CONPROF_INTERNAL_REVCOUNT}"
    fi

    export PYTHON_CONPROF_VERSION=${VERSION}
fi

# write the generated version back to VERSION file which will be used in generation
# of binaries
echo -n "__version__ = \"${VERSION}\"" > ./blackfire_conprof/version.py
}
