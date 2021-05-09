#!/bin/bash

create_fetch_branch() {
    git checkout -b fetch_data
    git push origin -u fetch_data
}

create_new_pr() {
# Not used yet as I want to do the PR manually first and no need
    destination_branch=main
    # Retrieve repository URL
    repository_url="$(git remote get-url origin | sed -e 's/git@//' -e 's/.git//' -e 's/:/\//')"
    echo "Repository url $repository_url"
    if [[ $repository_url == github* ]]; then
    echo "Create new PR from $branch to $destination_branch"
        pr_url=https://$repository_url/compare/$destination_branch...$branch
    fi
}

branch_fetch="fetch_data"
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" == "main" ]]; then
# Initialisation of the process
# If branch main, ie not current PR so create one
    echo "Current branch is main"
    if [ `git branch --list $branch_fetch` ]; then
        echo "Branch name $branch_fetch already exists."
        git checkout $branch_fetch
        git fetch && git pull
    else
        create_fetch_branch
    fi

else 
# Normal process
# Current branch is not main so it is fetch_data -> need to merge PR and create new one
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch is not main, it is $current_branch"
    git fetch && git pull
    git add .
    git commit -m "Commit all remaning changes before merge"
    git push origin $current_branch
    git checkout main
    git fetch && git pull
    git merge --no-ff $current_branch
    echo "Merge of $current_branch"
    git branch -D $current_branch
    # Create again a new branch which will receive the updates of the data.csv
    create_fetch_branch

fi

