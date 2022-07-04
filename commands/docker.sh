#!/bin/bash

# Some utility functions for docker
# Bash doesnt have concept of private functions
function __get_container {
    # Drop first line, and then select the first selected value
    echo $(docker ps --format '{{.Names}} {{.Image}}' | fzf -q "$1" | awk '{print $1}')
}

function __get_image {
    # Drop first line, and then select the first selected value
    echo $(docker images | sed 1d | fzf -q "$1" | awk '{print $3}')
}

function dlogs() {
    local selected_container
    selected_container=$(__get_container)

    if [ -n "$selected_container" ]; then
        echo "Showing logs for: " $selected_container
        docker logs $selected_container
    fi
}

# sh for alpine containers
function dexecsh() {
    local selected_container
    selected_container=$(__get_container)

    if [ -n "$selected_container" ]; then
        echo "Trying use exec /usr/bin/sh into container: " $selected_container
        docker exec -it $selected_container /usr/bin/sh
    fi
}

# Bash into the container
function dexecbash() {
    local selected_container
    selected_container=$(__get_container)

    if [ -n "$selected_container" ]; then
        echo "Trying use exec /usr/bin/sh into container: " $selected_container
        docker exec -it $selected_container /usr/bin/bash
    fi
}

# Remove selected image
function drmi() {
    local selected_image
    selected_image=$(__get_image)

    if [ -n "$selected_image" ]; then
        docker rmi $selected_image
    fi
}