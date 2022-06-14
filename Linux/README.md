# Linux tips

## cd命令自动补全目录

```bash
cat << EOF >> ~/.bashrc

# Complete cd command
complete -d cd
EOF
```

## nohup不打印日志的方法

```bash
nohup sh run.sh > /dev/null 2>&1 &
```

## 清理系统缓存

```bash
sync
echo 3 > /proc/sys/vm/drop_caches
```

## 解决ssh连接慢的问题

1. ```vim /etc/ssh/sshd_config```
2. 修改```#UseDNS yes```为```UseDNS no```
