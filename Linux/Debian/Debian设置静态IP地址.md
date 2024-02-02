# debian设置静态IP地址

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

## 编辑网络配置文件

以管理员权限编辑网络配置文件。

```shell
sudo nano /etc/network/interfaces
```

在文件中添加类似以下的配置（替换成你的实际网络配置）：

```plaintext
auto eth0
iface eth0 inet static
    address 192.168.8.23
    netmask 255.255.255.0
    gateway 192.168.8.1
    dns-nameservers 192.168.8.1

iface eth0 inet6 static
    address fd08::23/64
    gateway fd08::1
    dns-nameservers fd08::1
```

## 重新启动网络服务

完成更改后，重新启动网络服务以应用新的配置。

```shell
sudo systemctl restart networking
```
