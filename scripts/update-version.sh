#!/bin/bash

set -eux

git fetch --tags --force
PREV_TAG=`git describe --tags --abbrev=0 remotes/origin/prod`
VERSION=""

# when executing this script with a git tag defined by buildkite, we are releasing to production
if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
    VERSION="$BUILDKITE_TAG"
# when executing this script on the master/staging branch, we are releasing internal versions
elif [[ ${BUILDKITE_BRANCH:-} == "master" || ${BUILDKITE_BRANCH:-} == "staging" ]]; then
    VERSION=${PREV_TAG}

     # if there are multiple revisions, append that revision number
    _REV_COUNT=$(git rev-list "${PREV_TAG}"..HEAD --count 2>/dev/null) || true
    if [[ ! -z "${_REV_COUNT:-}" ]]; then
        VERSION="${PREV_TAG}+internal.${_REV_COUNT}"
    fi
fi

# write the generated version back to VERSION file which will be used in generation
# of binaries
echo -n "__version__ = \"${VERSION}\"" > ./blackfire_conprof/version.py

