#!/usr/bin/env bash

set -ev

# get travis env
echo "TRAVIS_EVENT_TYPE: ${TRAVIS_EVENT_TYPE}"
echo "TRAVIS_BRANCH: ${TRAVIS_BRANCH}"
echo "TRAVIS_PULL_REQUEST_SLUG: ${TRAVIS_PULL_REQUEST_SLUG}"
echo "TRAVIS_PULL_REQUEST_BRANCH: ${TRAVIS_PULL_REQUEST_BRANCH}"

# set default variable if not in env
if [[ -z ${TRAVIS_EVENT_TYPE} ]]; then
    TRAVIS_EVENT_TYPE="push";
    echo "TRAVIS_EVENT_TYPE set to push";
fi

if [[ -z ${TRAVIS_BRANCH} ]]; then
    TRAVIS_BRANCH="master";
    echo "TRAVIS_BRANCH set to master";
fi

# check if this is a pull request or a push
if [[ ${TRAVIS_EVENT_TYPE} == "pull_request" ]]; then
    git clone https://github.com/${TRAVIS_PULL_REQUEST_SLUG} kalliope;
    BRANCH_TO_CLONE=${TRAVIS_PULL_REQUEST_BRANCH};
else
    # it's a push
    git clone https://github.com/kalliope-project/kalliope.git kalliope;
    BRANCH_TO_CLONE=${TRAVIS_BRANCH};
fi

echo "Branch to checkout: ${BRANCH_TO_CLONE}";
cd kalliope;
git checkout ${BRANCH_TO_CLONE};

# install
sudo python3 setup.py install

# tests
python3 -m unittest discover
