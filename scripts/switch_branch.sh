#!/bin/bash

echo "$(git status)"
if [ `git branch --list $branch_fetch` ]; then
    echo "Branch name $branch_fetch exists, checkout to it."
    git checkout $branch_fetch
    git fetch && git pull
else
    ./scripts/branch.sh
fi