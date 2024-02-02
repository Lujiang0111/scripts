# Linux tips

## nohup不打印日志的方法

```shell
nohup sh run.sh > /dev/null 2>&1 &
```

## nohup运行python脚本

+ python添加```-u```参数，不启用输出缓冲

```shell
nohup python3 -u record_pid_top_stats.py 5524 1 &
```

## 临时添加/删除默认网关

```shell
route add default gw 192.168.1.1
route del default gw 192.168.1.1
```

## 禁止系统自动获取IPv6

```shell
sudo vim /etc/sysctl.conf
```

在文件末尾加入

```ini
# disable ipv6 autoconf
net.ipv6.conf.enp1s0.autoconf=0
net.ipv6.conf.enp1s0.accept_ra=0
net.ipv6.conf.enp1s0.use_tempaddr=0
```

重启系统或执行

```shell
sysctl -p
```

生效
