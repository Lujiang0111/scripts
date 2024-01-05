# Linux tips

## nohup不打印日志的方法

```shell
nohup sh run.sh > /dev/null 2>&1 &
```

## 临时添加/删除默认网关

```shell
route add default gw 192.168.1.1
route del default gw 192.168.1.1
```
