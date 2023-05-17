#!/usr/bin/env bash
set -e

BASE="$(dirname "$(dirname "$(readlink -f "$0")")")"

USER_ID=$(stat -c %u ${BASE})
GROUP_ID=$(stat -c %g ${BASE})

# site-packages are located under /usr/local
chown -R ${USER_ID}:${GROUP_ID} /usr/local

# change to user node
gosu ${USER_ID}:${GROUP_ID} "$@"
