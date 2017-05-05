#!/usr/bin/env bash

# get travis env
echo "TRAVIS_EVENT_TYPE: ${TRAVIS_EVENT_TYPE}"
echo "TRAVIS_BRANCH: ${TRAVIS_BRANCH}"
echo "TRAVIS_PULL_REQUEST_SLUG: ${TRAVIS_PULL_REQUEST_SLUG}"
echo "TRAVIS_PULL_REQUEST_BRANCH: ${TRAVIS_PULL_REQUEST_BRANCH}"

# set default variable if not in env
if [ -z ${TRAVIS_EVENT_TYPE} ]; then
TRAVIS_EVENT_TYPE="push";
echo "TRAVIS_EVENT_TYPE set to push";
fi

if [ -z ${TRAVIS_BRANCH} ]; then
TRAVIS_BRANCH="master";
echo "TRAVIS_BRANCH set to master";
fi

# check if this is a pull request or a push
if [ ${TRAVIS_EVENT_TYPE} == "pull_request" ]; then
    git clone https://github.com/${TRAVIS_PULL_REQUEST_SLUG} kalliope;
    cd kalliope;
    git checkout ${TRAVIS_PULL_REQUEST_BRANCH};
else
    # it's a push
    git clone https://github.com/kalliope-project/kalliope.git kalliope;
    cd kalliope;
    git checkout ${TRAVIS_BRANCH};
fi

# install
sudo python setup.py install

# tests
python -m unittest discover
