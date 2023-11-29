# Ros初始配置

## 设置网口与LAN IP

1. 规划好网口与地址分配
    + 网口分配：
      + 1号口 - 2.5G，做```LAN```口。
      + 2号口 - 做```wan```口。
      + 3号口 - 做```IPTV```口。
      + 其余均为```LAN```口。
    + 地址分配：
        + IPv4：ros地址```192.168.8.1```, 自建dns地址```192.168.8.5```，DHCP地址池```192.168.8.100-192.168.8.239```。
        + IPv6：ros地址```fd08::1```，自建dns地址```fd08::5```，内网地址池```fd08::/64```

2. 确定WAN口与LAN口。
    + 打开winbox，使用MAC地址方式连接至ros。
    + 点击**Interface**，选择**Interface**选项卡，确定WAN口、2.5G口、SFP口等，修改网口名称，方便记忆。
      + 1号口 - ```ether1-2.5g```
      + 2号口 - ```ether2-wan```
      + 3号口 - ```ether3-iptv```

3. 设置LAN网桥。
    + 点击**Bridge**，选择**Bridge**选项卡，创建一个Interface。Name填写```bridge-lan```。
    + 选择**Ports**选项卡，创建New Bridge Port，Interface选择LAN网口，Bridge选择```bridge-lan```，依次将1、4、5、6...口添加至网桥

4. 设定Interface List
    + 点击**Interface**，选择**Interface List**选项卡，添加一个Interface List，其中**List**选择```WAN```，**Interface**选择```ether2-wan```。
    + 点击**Interface**，选择**Interface List**选项卡，添加一个Interface List，其中**List**选择```LAN```，**Interface**选择```bridge-lan```。

5. 设置LAN IP。
    + 点击**IP**->**Addresses**，创建一个Address。Address填写想要分配的LAN IP```192.168.8.1/24```，Interface选择```bridge-lan```，设置完成后winbox就可以使用ip登录了。

## 设置拨号上网

1. 拨号上网设置。
    + 点击**Interface**，选择**Interface**选项卡，点击+号，选择**PPPOE Client**,新建一个PPPOE Client。选择**General**选项卡，Interfaces选择WAN口(```ether2-wan```)；选择Dial Out选项卡，User和Password填写拨号的用户名和密码，勾选```Add Default Route```

2. 设置IP伪装
    + 点击**IP**->**Firewall**，选择**NAT**选项卡，添加一条NAT规则。选择General选项卡，Chain选择```srcnat```；选择Action选项卡，Action选择```masquerade```，**取消**勾选Log。

## 设置DHCP

1. 设置DHCP IP池。
    + 点击**IP**->**Pool**，选择**Pools**选项卡，创建一个IP Pool。Name填写```pool-ipv4```，Addresses填写想要分配的地址池```192.168.8.100-192.168.8.239```，Next Pool选择```none```。

2. 设置DHCP
    + 点击**IP**->**DHCP Server**，选择**DHCP**选项卡，创建一个DHCP Server。选择General选项卡，Name填写```server-ipv4```，Interface选择```bridge-lan```，Address Pool选择```pool-ipv4```。
    + 选择**Networks**选项卡，新建一个DHCP Network。Address填写```192.168.8.0/24```，Gateway填写```192.168.8.1```，DNS Servers填写```192.168.8.1```

## 设置DNS

1. 设置DNS地址与DNS缓存
    + 点击**IP**->**DNS**，Server填写```223.5.5.5```,```223.6.6.6```，勾选```Allow Remote Requests```。

## 设置IPv6

1. 点击**Interface**，选择**Interface**选项卡，查看已创建的PPPOE Client，记录下```Actual MTU```列中的实际MTU值，本文以```1492```为例。

2. 点击**IPv6**->**DHCP Client**，点击+号，添加一个DHCPv6 Client，选择**DHCP**选项卡，Interface选择已创建的PPPOE Client，Request勾选```prefix```，Pool name填写```pool-ipv6```，Pool Prefix Length填```60```（电信：56，移动、联通：60），**取消**勾选```Use Peer DNS```，**取消**勾选```Add Default Route```，然后点右边的**Apply**，如果Prefix正确的话会显示状态栏**Status:Bound**，如果不正确就换个值再尝试。

3. 给网桥接口分配公网IPv6地址：点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address，Address填写```::/64```，From Pool选择```pool-ipv6```，Interface选择```bridge-lan```，勾选```EUI64```、```Advertise```。

4. 给网桥接口分配私有IPv6地址：点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address，Address填写```fd08::1/64```，Interface选择```bridge-lan```，勾选```Advertise```。

5. 设置IPv6伪装：点击**IPv6**->**Firewall**，选择**NAT**选项卡，添加一条NAT规则。选择General选项卡，Chain选择```srcnat```；选择Action选项卡，Action选择```masquerade```，**取消**勾选Log。

6. 点击**IPv6**->**ND**，选择**Interface**选项卡，选择默认的all规则，点击**Disable**禁用。点击+号，添加新的ND，Interface选择```bridge-lan```，RA Interval填写```60-120```，MTU填写之前查到的实际MTU值```1492```，DNS Servers填写```fd08::1```。

7. 点击**IPv6**->**ND**，选择**Prefixes**选项卡，点击**Default**，Valid Lifetime设置为```1d 00:00:00```，Preferred Lifetime设置为```00:12:00```。

## 开启UPnP（不建议）

1. 点击**IP**->**UPnp**，勾选```Enabled```、```Allow To Disable External Interface```、```Show Dummy Rule```。

2. 点击Interfaces，创建一个Upnp，Interface选择WAN口(```ether2-wan```)，type选择```external```。

3. 点击Interfaces，创建一个Upnp，Interface选择```bridge-lan```，type选择```internal```。

## 防火墙设置

以下配置均为ROS默认自带防火墙规则（去掉了fasttrack，会导致卡顿）

1. IPv4防火墙：

    ```ros
    /ip firewall filter add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    /ip firewall filter add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
    /ip firewall filter add chain=input action=accept protocol=icmp comment="defconf: accept ICMP"
    /ip firewall filter add chain=input action=accept dst-address=127.0.0.1 comment="defconf: accept to local loopback (for CAPsMAN)"
    /ip firewall filter add chain=input action=drop in-interface-list=!LAN comment="defconf: drop all not coming from LAN"
    /ip firewall filter add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept in ipsec policy"
    /ip firewall filter add chain=forward action=accept ipsec-policy=out,ipsec comment="defconf: accept out ipsec policy"
    /ip firewall filter add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related, untracked"
    /ip firewall filter add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
    /ip firewall filter add chain=forward action=drop connection-state=new connection-nat-state=!dstnat in-interface-list=WAN comment="defconf: drop all from WAN not DSTNATed"
    ```

2. IPv6防火墙

    ```ros
    /ipv6 firewall address-list add list=bad_ipv6 address=::/128 comment="defconf: unspecified address"
    /ipv6 firewall address-list add list=bad_ipv6 address=::1 comment="defconf: lo"
    /ipv6 firewall address-list add list=bad_ipv6 address=fec0::/10 comment="defconf: site-local"
    /ipv6 firewall address-list add list=bad_ipv6 address=::ffff:0:0/96 comment="defconf: ipv4-mapped"
    /ipv6 firewall address-list add list=bad_ipv6 address=::/96 comment="defconf: ipv4 compat"
    /ipv6 firewall address-list add list=bad_ipv6 address=100::/64 comment="defconf: discard only "
    /ipv6 firewall address-list add list=bad_ipv6 address=2001:db8::/32 comment="defconf: documentation"
    /ipv6 firewall address-list add list=bad_ipv6 address=2001:10::/28 comment="defconf: ORCHID"
    /ipv6 firewall address-list add list=bad_ipv6 address=3ffe::/16 comment="defconf: 6bone"
    /ipv6 firewall filter add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    /ipv6 firewall filter add chain=input action=drop connection-state=invalid comment="defconf: drop invalid"
    /ipv6 firewall filter add chain=input action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
    /ipv6 firewall filter add chain=input action=accept protocol=udp port=33434-33534 comment="defconf: accept UDP traceroute"
    /ipv6 firewall filter add chain=input action=accept protocol=udp dst-port=546 src-address=fe80::/10 comment="defconf: accept DHCPv6-Client prefix delegation."
    /ipv6 firewall filter add chain=input action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
    /ipv6 firewall filter add chain=input action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
    /ipv6 firewall filter add chain=input action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
    /ipv6 firewall filter add chain=input action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
    /ipv6 firewall filter add chain=input action=drop in-interface-list=!LAN comment="defconf: drop everything else not coming from LAN"
    /ipv6 firewall filter add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked"
    /ipv6 firewall filter add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid"
    /ipv6 firewall filter add chain=forward action=drop src-address-list=bad_ipv6 comment="defconf: drop packets with bad src ipv6"
    /ipv6 firewall filter add chain=forward action=drop dst-address-list=bad_ipv6 comment="defconf: drop packets with bad dst ipv6"
    /ipv6 firewall filter add chain=forward action=drop protocol=icmpv6 hop-limit=equal:1 comment="defconf: rfc4890 drop hop-limit=1"
    /ipv6 firewall filter add chain=forward action=accept protocol=icmpv6 comment="defconf: accept ICMPv6"
    /ipv6 firewall filter add chain=forward action=accept protocol=139 comment="defconf: accept HIP"
    /ipv6 firewall filter add chain=forward action=accept protocol=udp dst-port=500,4500 comment="defconf: accept IKE"
    /ipv6 firewall filter add chain=forward action=accept protocol=ipsec-ah comment="defconf: accept ipsec AH"
    /ipv6 firewall filter add chain=forward action=accept protocol=ipsec-esp comment="defconf: accept ipsec ESP"
    /ipv6 firewall filter add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept all that matches ipsec policy"
    /ipv6 firewall filter add chain=forward action=drop in-interface-list=!LAN comment="defconf: drop everything else not coming from LAN"
    ```

## 安全设置

1. 关闭不必要的服务
    + 点击**IP**->**Services**，只留下winbox与www
    + 分别点击**winbox**与**www**,Available from项填写```192.168.0.0/16```（只允许内网访问）。

2. 设置管理员密码
    + 点击**System**->**Users**，设置admin的密码。

3. 升级固件
    + 点击**System**->**Packages**，点击**Check For Updates**查找更新，一般选择stable通道。
