#! /usr/bin/env bash

function abcli_aws_batch_list() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local queue=$(abcli_option "$options" queue abcli-v3)
    local prefix=$(abcli_option "$options" prefix)
    local show_count=$(abcli_option_int "$options" count 1)
    local status=$(abcli_option "$options" status)

    local pipes=""
    [[ ! -z "$prefix" ]] && pipes="| grep $prefix"
    [[ "$show_count" == 1 ]] && pipes="$pipes | wc -l | python3 -m blueflow.aws_batch show_count"

    [[ -z "$status" ]] && status=$(echo $ABCLI_AWS_BATCH_JOB_STATUS_LIST_WATCH | tr , " ")

    abcli_badge "🌀"

    abcli_log "queue: $queue"
    local status_
    for status_ in $status; do
        [[ "$show_count" == 1 ]] && abcli_log "status: $status_"
        abcli_eval dryrun=$do_dryrun,log=$(abcli_not $show_count) \
            "aws batch list-jobs \
                --job-status $status_ \
                --job-queue $queue \
                --output text \
                $pipes"
    done
}
