# linux常用脚本

## 循环运行停止进程

+ ```cycle_run_stop.sh```

```bash
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

cycle_time=0
while true; do
    ((cycle_time++))
    echo -e "\033[33mcycle ${cycle_time}, run ${exe_file}\033[0m"
    "${shell_dir}/${exe_file}" &
    pid=$!
    sleep "${run_duration}"

    echo -e "\033[33mcycle ${cycle_time}, kill ${pid}\033[0m"
    kill -9 ${pid}
    sleep "${stop_duration}"
done
```
