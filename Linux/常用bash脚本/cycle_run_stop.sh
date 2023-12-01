#!/bin/bash
shell_dir=$(cd "$(dirname "$0")" || exit;pwd)/

if [ $# -lt 3 ]; then
    echo -e "\033[33mUsage:\033[0m"
    echo -e "Args:\t\tsh cycle_run_stop.sh exe_file run_duration(s) stop_duration(s)"
    echo -e "Example: \tsh cycle_run_stop.sh smartd 60 60"
    exit 0
fi

exe_file=$1
run_duration=$2
stop_duration=$3
exe_file_pid=
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
    echo -e "\033[33mcycle ${cycle_time}, run ${exe_file}\033[0m"
    "${shell_dir}/${exe_file}" &
    exe_file_pid=$!

    if [ "$running" = true ]; then
        sleep "${run_duration}" &
        sleep_pid=$!
        wait ${sleep_pid}
        sleep_pid=
    fi

    echo -e "\033[33mcycle ${cycle_time}, kill ${exe_file_pid}\033[0m"
    kill -9 ${exe_file_pid}
    exe_file_pid=

    if [ "$running" = true ]; then
        sleep "${stop_duration}" &
        sleep_pid=$!
        wait ${sleep_pid}
        sleep_pid=
    fi
done
