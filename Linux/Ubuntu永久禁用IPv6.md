# Ubuntu永久禁用IPv6

使用root权限编辑```/etc/default/grub```文件

```bash
sudo vim /etc/default/grub
```

寻找```GRUB_CMDLINE_LINUX_DEFAULT```配置项

```ini
GRUB_CMDLINE_LINUX_DEFAULT=""
```

添加```ipv6.disable=1```启动参数

```ini
GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1"
```

更新grub

```bash
sudo update-grub
```

重启系统

```bash
sudo init 6
```

修改完成
