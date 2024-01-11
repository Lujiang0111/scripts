# 常用bash脚本

## 循环运行停止进程

+ 文件名 : ```cycle_run_stop.sh```
+ 使用方式：
  + ```sh cycle_run_stop.sh exe_file run_duration(s) stop_duration(s)```

```shell
bash cycle_run_stop.sh smartd 60 60
```

## ssh保活

+ 文件名 : ```ssh_keep_alive.sh```
+ 使用方式：
  + ```sh ssh_keep_alive.sh [sleep_duration(s)]```

```shell
bash ssh_keep_alive.sh 30
```
