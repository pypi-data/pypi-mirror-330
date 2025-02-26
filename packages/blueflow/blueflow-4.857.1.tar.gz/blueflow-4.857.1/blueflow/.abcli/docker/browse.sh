#! /usr/bin/env bash

function abcli_docker_browse() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local show_public=$(abcli_option_int "$options" public 1)

    local url="https://hub.docker.com/repository/docker/kamangir/abcli/general"
    [[ "$show_public" == 1 ]] &&
        local url="https://hub.docker.com/r/kamangir/abcli/tags"

    abcli_browse $url
}
