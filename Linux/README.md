# Linux tips

## cd命令自动补全目录

```shell
cat << EOF >> ~/.bashrc

# Complete cd command
complete -d cd
EOF
```

## nohup不打印日志的方法

```shell
nohup sh run.sh > /dev/null 2>&1 &
```

## 清理系统缓存

```shell
sync
echo 3 > /proc/sys/vm/drop_caches
```

## 解决ssh连接慢的问题

1. ```vim /etc/ssh/sshd_config```
2. 修改```#UseDNS yes```为```UseDNS no```

## CentOS7最小化安装后网络设置

1. 输入```nmcli d```命令快速查看网卡列表以及连接情况。
2. 输入```nmtui```命令进入图形化网络设置界面，选择对应网卡，设置Ip（x.x.x.x/xx格式），网关，dns，dhcp。
3. 输入```service network restart```重启网络。
