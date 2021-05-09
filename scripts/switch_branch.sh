#!/bin/bash

echo "$(git status)"
if [ `git branch --list $branch_fetch` ]; then
    echo "Branch name $branch_fetch exists, checkout to it."
    current_branch="$(git rev-parse --abbrev-ref HEAD)"
    if [[ "$current_branch" != "fetch_data" ]]; then
        git checkout $branch_fetch
        git fetch && git pull
    fi
else
    ./scripts/branch.sh
fi