#!/bin/bash
set -euo pipefail

git fetch --tags

channel="testing"
if [[ ${BUILDKITE_TAG:-""} != "" ]]; then
    channel="stable"
fi

grep_options=""

if [ "$channel" == "stable" ]
then
    grep_options="-v"
fi

# At this point, the current commit has been tagged previously
# by tag_repo.sh
previous_tag=$(git for-each-ref --sort='-creatordate' --format '%(refname:short)' --no-contains HEAD refs/tags \
               | grep $grep_options 'internal' \
               | head -n 1)

# Ignore if file is empty, because it will be empty for first deployment
echo "+++ Notify chatbot"

# Get the script
curl --fail -o mark-prs.sh \
    --user "bot:$CHATBOT_PASSWORD" \
    https://chatbot.private.blackfire.io/api/release/script

chmod a+x mark-prs.sh

export RELEASE_REV_OLD="$previous_tag"
export RELEASE_CHANNEL="$channel"
export RELEASE_API_PASSWORD="${CHATBOT_PASSWORD}"
export RELEASE_COMPONENT="python-conprof"

./mark-prs.sh

rm mark-prs.sh
