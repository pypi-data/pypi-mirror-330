#! /usr/bin/env bash

function abcli_docker_build() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_push=$(abcli_option_int "$options" push $(abcli_not $do_dryrun))
    local do_run=$(abcli_option_int "$options" run 0)
    local no_cache=$(abcli_option_int "$options" no_cache 0)
    local verbose=$(abcli_option_int "$options" verbose 0)

    abcli_badge "🪄🌠"
    abcli_log "@docker: build $options ..."

    pushd $abcli_path_git >/dev/null

    mkdir -p temp
    cp -v ~/.kaggle/kaggle.json temp/

    local extra_args=""
    [[ "$verbose" == 1 ]] &&
        extra_args="$extra_args --progress=plain"
    [[ "$no_cache" == 1 ]] &&
        extra_args="$extra_args --no-cache"

    abcli_eval ,$options \
        docker build \
        --platform=linux/amd64 \
        $extra_args \
        --build-arg HOME=$HOME \
        -t kamangir/abcli \
        -f notebooks-and-scripts/Dockerfile \
        .
    [[ $? -ne 0 ]] && return 1

    rm -rfv temp

    if [[ "$do_push" == "1" ]]; then
        abcli_docker_push $options
        [[ $? -ne 0 ]] && return 1
    fi

    if [[ "$do_run" == "1" ]]; then
        abcli_docker_run $options
        [[ $? -ne 0 ]] && return 1
    fi

    popd >/dev/null
}
