#!/bin/bash

set -eux

#!/bin/bash

set -eu

git fetch --tags --force

PREV_TAG=`git describe --tags --abbrev=0`
REV_COUNT=""
VERSION=""

# when executing this script with a git tag defined by buildkite, we are releasing to production
if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
    VERSION="$BUILDKITE_TAG"
# when executing this script on the master branch, we are releasing internal versions
elif [[ ${BUILDKITE_BRANCH:-} != "master" ]]; then
    VERSION=${PREV_TAG}

     # if there are multiple revisions, append that revision number
    _REV_COUNT=$(git rev-list "${PREV_TAG}"..HEAD --count 2>/dev/null) || true
    if [[ ! -z "${_REV_COUNT:-}" ]]; then
        REV_COUNT=${_REV_COUNT}
    fi

    if [[ ${REV_COUNT} != "" ]]; then
        VERSION="${PREV_TAG}+internal.${REV_COUNT}"
    fi
fi

# write the generated version back to VERSION file which will be used in generation
# of binaries
echo -n "__version__ = \"${VERSION}\"" > ./blackfire_conprof/version.py

