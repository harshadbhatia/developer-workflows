#!/bin/bash

# Utilties functions for git

function __get_branch {
    echo $(git branch | fzf)
}

function gitco() {

    local selected_branch
    selected_branch=$(__get_branch)

    git checkout $selected_branch

}

function gitrebase() {
    git fetch origin master

    gitco

    git rebase origin/master

}