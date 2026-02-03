#!/bin/bash

set -eux

git fetch --tags --force
PREV_TAG=`git describe --tags --abbrev=0`
VERSION=""

echo "Previous tag is ${PREV_TAG}"

if [[ ${RELEASE_VERSION:-""} != "" ]]; then
    if [[ ${RELEASE_VERSION} == "master" ]]; then
        VERSION=${PREV_TAG}

        # if there are multiple revisions, append that revision number
        _REV_COUNT=$(git rev-list "${PREV_TAG}"..HEAD --count 2>/dev/null) || true
        echo "REV_COUNT is ${_REV_COUNT}"
        if [[ ! -z "${_REV_COUNT:-}" ]]; then
            VERSION="${PREV_TAG}+internal.${_REV_COUNT}"
        fi
    else
        VERSION="${RELEASE_VERSION}"
    fi
fi

echo "VERSION is ${VERSION}"

# write the generated version back to VERSION file which will be used in generation
# of binaries
echo -n "__version__ = \"${VERSION}\"" > ./blackfire_conprof/version.py
