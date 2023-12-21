#!/bin/bash

sleep_pid=
running=true

function TrapSigint()
{
    running=false
    if [[ "x" != "${sleep_pid}x" ]]; then
        kill -9 "${sleep_pid}"
    fi
}
trap TrapSigint 2

cycle_time=0
while [ "$running" = true ]; do
    ((cycle_time++))
    echo -e "\033[33mcycle ${cycle_time}, keep alive\033[0m"

    if [ "$running" = true ]; then
        sleep 10 &
        sleep_pid=$!
        wait ${sleep_pid}
        sleep_pid=
    fi
done
