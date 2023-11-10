#!/bin/bash

set -eu

# This flag toggles the release destination to testing.pypi.org if set to true
DEPLOY_TESTPYPI=false

packagecloud_package_name=python-conprof

# yank all internal versions from packageloud.io/testing
if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
    packagecloud_repo='stable'
else
    packagecloud_repo='testing'
fi

# include packagecloud credentials
if [ -f /etc/secret/package-cloud.sh ]; then
    source /etc/secret/package-cloud.sh
else
    echo "WARNING: no file named /etc/secret/package-cloud.sh was found"
fi

function release()
{
    wheel_path="$1"

    if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
        export TWINE_PASSWORD="`cat /etc/secret/pypi-token.password`"
        if [ "$DEPLOY_TESTPYPI" = true ] ; then
            export TWINE_REPOSITORY_URL="https://test.pypi.org/legacy/"
            export TWINE_PASSWORD="`cat /etc/secret/pypi-test-token.password`"
        fi

        twine upload $wheel_path/*.whl --verbose
    else
        package_cloud push blackfire-io/${packagecloud_repo}/${packagecloud_package_name} $wheel_path/*.whl
    fi
}

function yank_all()
{
    packages=`curl -sG -H 'Host: packagecloud.io' https://packagecloud.io/blackfire-io/${packagecloud_repo}/pypi/simple/blackfire | sed -n 's/.*href="\([^"]*\).*$/\1/p#' | xargs -i sh -c 'basename {}'`
    for package in ${packages}
    do
        echo "Yanking \"${package}\""
        package_cloud yank blackfire-io/${packagecloud_repo}/${packagecloud_package_name} ${package} || true
    done
}
