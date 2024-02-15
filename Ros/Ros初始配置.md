# Ros初始配置

## 设置网口与LAN IP

### 规划好网口与地址分配
  
+ 网口分配：
  + 1号口 - 2.5G，做`lan`口。
  + 2号口 - 做`wan`口，接光猫。
  + 3号口 - 做`iptv`口。
  + 其余均为`lan`口。

+ 地址分配：
  + 光猫：地址`192.168.100.1`
  + IPv4：ros地址`192.168.8.1`, 自建dns地址`192.168.8.5`，DHCP地址池`192.168.8.100-192.168.8.239`。
  + IPv6：ros地址`fd08::1`，自建dns地址`fd08::5`，内网地址池`fd08::/64`

### 使用winbox连接至ros

+ winbox是ros官方提供的图形化管理工具，下载地址：<https://mikrotik.com/download>
+ 打开winbox，选择使用mac地址方式连接至ros。

### 修改接口名称

点击**Interfaces**，选择**Interface**选项卡，确定wan口、2.5G口、SFP口等，修改网口名称，方便记忆。

+ 1号口 - `ether1-2.5g`
+ 2号口 - `ether2-wan`
+ 3号口 - `ether3-iptv`

### 设置LAN网桥

+ 点击**Bridge**，选择**Bridge**选项卡，创建一个bridge：
  + **Name** - `bridge-lan`
  + **IGMP Snooping** - ✔
+ 点击**Bridge**，选择**Ports**选项卡，创建New Bridge Port：
  + **Interface** - `lan网口`
  + **Bridge** - `bridge-lan`
  依次将1、4、5、6...口添加至网桥。

### 添加Interface List

+ 点击**Interfaces**，选择**Interface List**选项卡，点击**list**按钮，进入**Interface Lists**页面，添加`WAN`（外网）和`LAN`（内网）和`ONU`（光猫）

+ 点击**Interfaces**，选择**Interface List**选项卡，添加一个Interface List：
  + **List** - `ONU`
  + **Interface** - `ether2-wan`
+ 点击**Interfaces**，选择**Interface List**选项卡，添加一个Interface List：
  + **List** - `LAN`
  + **Interface** - `bridge-lan`

### 设置lan口IP

+ 点击**IP**->**Addresses**，添加一个LAN口IP：
  + **Address** - `192.168.8.1/24`
  + **Interface** - `bridge-lan`

## 安全设置

### 关闭不必要的服务

+ 点击**IP**->**Services**，只留下winbox与www
+ 分别点击**winbox**与**www**：
  + **Available from** - `192.168.0.0/16`（只允许内网访问）。

### 设置时钟同步

+ 点击**System**->**NTP Client**，添加NTP Server：
  + cn.ntp.org.cn
  + cn.pool.ntp.org
  + ntp.aliyun.com
  + ntp.tencent.com
+ 点击**System**->**Clock**
  + **Time Zone Name** - `Asia/Shanghai`。

### 设置连接属性

```shell
/ip firewall connection tracking {
  set tcp-syn-sent-timeout=120s
  set tcp-syn-received-timeout=60s
  set tcp-established-timeout=7440s
  set tcp-fin-wait-timeout=120s
  set tcp-close-wait-timeout=60s
  set tcp-last-ack-timeout=30s
  set tcp-time-wait-timeout=120s
  set tcp-close-timeout=10s
  set tcp-max-retrans-timeout=300s
  set tcp-unacked-timeout=300s
  set udp-timeout=30s
  set udp-stream-timeout=120s
  set icmp-timeout=30s
  set generic-timeout=600s
}
```

## 防火墙设置

+ IPv4防火墙：

```shell
/ip firewall {
    filter add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    filter add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
    filter add chain=input action=accept protocol=icmp comment="defconf: accept ICMP"
    filter add chain=input action=accept dst-address=127.0.0.1 comment="defconf: accept to local loopback (for CAPsMAN)"
    filter add chain=input action=drop in-interface-list=!LAN comment="defconf: drop all not coming from LAN"
    filter add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept in ipsec policy"
    filter add chain=forward action=accept ipsec-policy=out,ipsec comment="defconf: accept out ipsec policy"
    filter add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related, untracked"
    filter add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
    filter add chain=forward action=drop connection-state=new connection-nat-state=!dstnat in-interface-list=WAN comment="defconf: drop all from WAN not DSTNATed"
    filter add chain=forward action=drop connection-state=new connection-nat-state=!dstnat in-interface-list=ONU comment="defconf: drop all from ONU not DSTNATed"
}
```

+ IPv6防火墙

```shell
/ipv6 firewall {
    address-list add list=bad_ipv6 address=::/128 comment="defconf: unspecified address"
    address-list add list=bad_ipv6 address=::1 comment="defconf: lo"
    address-list add list=bad_ipv6 address=fec0::/10 comment="defconf: site-local"
    address-list add list=bad_ipv6 address=::ffff:0:0/96 comment="defconf: ipv4-mapped"
    address-list add list=bad_ipv6 address=::/96 comment="defconf: ipv4 compat"
    address-list add list=bad_ipv6 address=100::/64 comment="defconf: discard only "
    address-list add list=bad_ipv6 address=2001:db8::/32 comment="defconf: documentation"
    address-list add list=bad_ipv6 address=2001:10::/28 comment="defconf: ORCHID"
    address-list add list=bad_ipv6 address=3ffe::/16 comment="defconf: 6bone"
}
```

```shell
/ipv6 firewall {
    filter add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    filter add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
    filter add chain=input action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
    filter add chain=input action=accept protocol=udp port=33434-33534 comment="defconf: accept UDP traceroute"
    filter add chain=input action=accept protocol=udp dst-port=546 src-address=fe80::/10 comment="defconf: accept DHCPv6-Client prefix delegation."
    filter add chain=input action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
    filter add chain=input action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
    filter add chain=input action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
    filter add chain=input action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
    filter add chain=input action=drop in-interface-list=!LAN comment="defconf: drop everything else not coming from LAN"
    filter add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    filter add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
    filter add chain=forward action=drop src-address-list=bad_ipv6 comment="defconf: drop packets with bad src ipv6"
    filter add chain=forward action=drop dst-address-list=bad_ipv6 comment="defconf: drop packets with bad dst ipv6"
    filter add chain=forward action=drop protocol=icmpv6 hop-limit=equal:1 comment="defconf: rfc4890 drop hop-limit=1"
    filter add chain=forward action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
    filter add chain=forward action=accept protocol=139 comment="defconf: accept HIP"
    filter add chain=forward action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
    filter add chain=forward action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
    filter add chain=forward action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
    filter add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
    filter add chain=forward action=drop in-interface-list=!LAN comment="defconf: drop everything else not coming from LAN"
}
```

## 设置拨号上网

### 添加pppoe client

+ 点击**Interfaces**，选择**Interface**选项卡，点击+号，选择**PPPOE Client**,新建一个PPPOE Client：
  + **General**
    + **Name** - `pppoe-bjlt`
    + **Interfaces** - `ether2-wan`
  + **Dial Out**
    + **User** - pppoe用户名
    + **Password** - pppoe密码
    + **Add Default Route** - ✔

### 设置Interface List

+ 点击**Interfaces**，选择**Interface List**选项卡，添加一个Interface List：
  + **List** - `WAN`
  + **Interface** - `pppoe-bjlt`

### 设置wan口IP伪装

```shell
/ip firewall nat add action=masquerade chain=srcnat comment="defconf: masquerade IPv4"
```

## 设置DHCP

### 设置DHCP IP池

+ 点击**IP**->**Pool**，选择**Pools**选项卡，创建一个IP Pool：
  + **Name** - `pool-ipv4`
  + **Addresses** - `192.168.8.100-192.168.8.239`（想要分配的地址池）

### 设置DHCP Server

+ 点击**IP**->**DHCP Server**，选择**DHCP**选项卡，创建一个DHCP Server：
  + **Name** - `server-ipv4`
  + **Interface** - `bridge-lan`
  + **Address Pool** - `pool-ipv4`
+ 点击**IP**->**DHCP Server**，选择**Networks**选项卡，新建一个DHCP Network：
  + **Address** - `192.168.8.0/24`
  + **Gateway** - `192.168.8.1`
  + **DNS Servers** - `192.168.8.1`

## 设置DNS地址与DNS缓存

+ 点击**IP**->**DNS**：
  + **Server** - `223.5.5.5`,`119.29.29.29`
  + **Allow Remote Requests** - ✔

## 设置IPv6

+ 点击**Interfaces**，选择**Interface**选项卡，查看已创建的PPPOE Client，记录下`Actual MTU`列中的实际MTU值，本文以`1492`为例。

### 设置DHCPv6

+ 点击**IPv6**->**DHCP Client**，点击+号，添加一个DHCPv6 Client：
  + **DHCP**
    + **Interface** - `pppoe-bjlt`
    + **Request** - `prefix`
    + **Pool name** - `pool-ipv6`
    + **Pool Prefix Length** - `60`（电信：56，移动、联通：60）
    + **Use Peer DNS** - ❌
    点击**Apply**，如果Prefix正确的话会显示状态栏**Status:Bound**，如果不正确就换个**Pool Prefix Length**值再尝试。

### 给网桥接口分配公网IPv6地址

+ 点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address：
  + **Address** - `::/64`，
  + **From Pool** - `pool-ipv6`
  + **Interface** - `bridge-lan`
  + `EUI64` - ✔
  + `Advertise` - ✔

### 给网桥接口分配私有IPv6地址

+ 点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address：
  + **Address** - `fd08::1/64`，
  + **Interface** - `bridge-lan`
  + `Advertise` - ✔

### 设置IPv6伪装

```shell
/ipv6 firewall nat add action=masquerade chain=srcnat comment="defconf: masquerade IPv6"
```

### 设置IPv6 ND

+ 点击**IPv6**->**ND**，选择**Interface**选项卡，选择默认的all规则，点击**Disable**禁用。

+ 点击**IPv6**->**ND**，选择**Interface**选项卡，点击+号，添加新的ND：
  + **Interface** - `bridge-lan`
  + **MTU** - 填写之前查到的实际MTU值`1492`
  + **DNS Servers** - `fd08::1`

+ 点击**IPv6**->**ND**，选择**Prefixes**选项卡，点击**Default**：
  + **Valid Lifetime** - `2d 00:00:00`
  + **Preferred Lifetime** - `1d 00:00:00`

## 设置访问光猫网段

### 设置wan口IP

+ 点击**IP**->**Address**，添加一个wan口IP（注意wab口IP和光猫需在同一网段,例如`192.168.100.2`）：
  + **Address** - `192.168.100.2/24`
  + **Interface** - `ether2-wan`

### 添加防火墙规则

```shell
/ip firewall mangle add action=accept chain=prerouting comment="onuconf: access to ONU" src-address=192.168.8.0/24 dst-address=192.168.100.0/24
```

## 开启UPnP（不建议）

+ 点击**IP**->**UPnp**，勾选`Enabled`、`Allow To Disable External Interface`、`Show Dummy Rule`。

+ 点击Interfaces，创建一个Upnp，Interface选择wan口(`ether2-wan`)，type选择`external`。

+ 点击Interfaces，创建一个Upnp，Interface选择`bridge-lan`，type选择`internal`。

## 可选配置

+ ip neighbor

```shell
/ip neighbor discovery-settings set discover-interface-list=LAN
```

+ mac-server

```shell
/tool mac-server set allowed-interface-list=LAN
/tool mac-server mac-winbox set allowed-interface-list=LAN
```

+ 升级固件
  + 点击**System**->**Packages**，点击**Check For Updates**查找更新，一般选择stable通道。
