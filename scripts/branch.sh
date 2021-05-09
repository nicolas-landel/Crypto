#!/bin/bash

create_new_branch() {
    git checkout -b fetch_data
    git push origin -u fetch_data
    branch=fetch_data
}

create_new_pr() {
# Not used yet as I want to do the PR manually first
    destination_branch=main
    # Retrieve repository URL
    repository_url="$(git remote get-url origin | sed -e 's/git@//' -e 's/.git//' -e 's/:/\//')"
    echo "Repository url $repository_url"
    if [[ $repository_url == github* ]]; then
    echo "Create new PR from $branch to $destination_branch"
        pr_url=https://$repository_url/compare/$destination_branch...$branch
    fi
}

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "main" ]]; then
# If branch main, ie not current PR so create one
    echo "Current branch is main"
    create_new_branch

else 
# Current branch is not main so it is fetch_data -> need to merge PR and create new one
    current_branch = $(git rev-parse --abbrev-ref HEAD)
    echo "Current branch is not main, it is $current_branch"
    git fetch && git pull
    git checkout main
    git fetch && git pull
    # git merge --no-ff $current_branch
    # git branch -D $current_branch


fi

