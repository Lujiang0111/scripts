# Ros配置WireGuard

> 参考资料：<https://www.truenasscale.com/2022/04/30/1032.html>

+ 内网网段：```192.168.8.0/24```
+ WireGuard网段：```192.168.9.0/24```

## 生成Peer公钥

+ 我们需要借助别的客户端生成Peer的秘钥，使用的Windows的WireGuard的软件，点击**新建空隧道**，然后它就会自动的生成私钥和公钥，这里假设公钥为```public-key-peer```。

## Ros设置

### 设置ddns

+ 点击**IP**->**Cloud**，选择**Cloud**选项卡，点击+号。
  + DDNS Enabled - ```✔```
  + Update Time - ```✔```

+ 点击```apply```确认后，DNS Name区域会生成一段网址```xxx.sn.mynetname.net```，使用nslookup命令查看网址即可查询对应的公网IP。

### 设置WireGuard

+ 点击**WireGuard**，选择**WireGuard**选项卡，点击+号。
  + Name - ```wireguard-lan```
  + MTU - ```1500```
  + Listen Port - ```52321```

+ 添加完成后，可以看到**wireguard-lan**自动生成了一串**Public Key**，这里假设为```public-key-lan```。

### 防火墙放行wireguard-lan

+ ROS默认规则有一条```defconf: drop all not coming from LAN```，需要在此规则前加一条对**wireguard-lan**的**Listen Port**的放行规则。

```shell
/ip/firewall/filter/add chain=input protocol=udp dst-port=52321 action=accept place-before=0 comment="accept wireguard listen port"
```

+ 将**wireguard-lan**添加到**LAN**中

```shell
/interface/list/member/add list=LAN interface=wireguard-lan
```

### 设置Peer

+ 点击**WireGuard**，选择**Peers**选项卡，点击+号。
  + Interface - ```wireguard-lan```
  + Public Key - ```public-key-peer```
  + Allowed Address - ```192.168.9.21/32```
  + Persistent Keepalive - ```00:00:25```

### 为WireGuard设置IP

+ 点击**IP**->**Addresses**，选择**Peers**选项卡，点击+号。
  + Address - ```192.168.9.1/24```
  + Interface - ```wireguard-lan```

## 客户端配置

+ 不同的客户端配置方法是大同小异的，我就以刚刚Windows生成的继续往下配置了，名称填写```wireguard-peer```。

```ini
[Interface]
PrivateKey = private-key-peer   # Windows自动生成的私钥
Address = 192.168.9.21/32      # Ros设置中为Peer设置的IP
DNS = 192.168.8.1               # Ros的DNS地址，可以不填
[peer]
PublicKey = public-key-lan      # wireguard-lan的公钥
Endpoint = 123.45.67.89:52321   # 这个填ROS的公网：监听端口
AllowedIPs = 192.168.8.0/21     # 填写需要通过WireGuard代理的地址段
PersistentKeepalive = 25        # 心跳间隔25s
```
