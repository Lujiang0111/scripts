# Ros初始配置

## 设置网口与LAN IP

1. 规划好网口与地址分配
    + 网口分配：2号网口为```wan口```，其余为```LAN口```。
    + 地址分配：
        + IPv4：ros地址```192.168.8.1```, 自建dns地址```192.168.8.3```，DHCP地址池```192.168.8.50-192.168.8.239```。
        + IPv6：ros地址```fd08::1```，自建dns地址```fd08::3```，内网地址池```fd08::/64```

2. 确定WAN口与LAN口。

    打开winbox，使用MAC地址方式连接至ros。

    点击**Interface**，选择**Interface**选项卡，确定WAN口、2.5G口、SFP口等。修改Name为```ether1-2.5g```、```ether2-wan```等，方便记忆。

3. 设置LAN网桥。

    点击**Bridge**，选择**Bridge**选项卡，创建一个Interface。Name填写```bridge-lan```。

    选择**Ports**选项卡，创建New Bridge Port，Interface依次选择LAN网口，Bridge选择```bridge-lan```，有多少个LAN口就要创建多少个bridge。

4. 设置LAN IP。

    点击**IP**->**Addresses**，创建一个Address。Address填写想要分配的LAN IP```192.168.8.1/24```，Interface选择```bridge-lan```，设置完成后winbox就可以使用ip登录了。

## 设置拨号上网

1. 拨号上网设置。

    点击**Interface**，选择**Interface**选项卡，点击+号，选择**PPPOE Client**,新建一个PPPOE Client。选择**General**选项卡，Interfaces选择WAN口(```ether2-wan```)；选择Dial Out选项卡，User和Password填写拨号的用户名和密码，勾选```Add Default Route```

2. 设置IP伪装

    点击**IP**->**Firewall**，选择**NAT**选项卡，添加一条NAT规则。选择General选项卡，Chain选择```srcnat```；选择Action选项卡，Action选择```masquerade```，**取消**勾选Log。

## 设置DHCP

1. 设置DHCP IP池。

    点击**IP**->**Pool**，选择**Pools**选项卡，创建一个IP Pool。Name填写```pool-ipv4```，Addresses填写想要分配的地址池```192.168.8.50-192.168.8.239```，Next Pool选择```none```。

2. 设置DHCP

    点击**IP**->**DHCP Server**，选择**DHCP**选项卡，创建一个DHCP Server。选择General选项卡，Name填写```server-ipv4```，Interface选择```bridge-lan```，Address Pool选择```pool-ipv4```。

    选择**Networks**选项卡，新建一个DHCP Network。Address填写```192.168.8.0/24```，Gateway填写```192.168.8.1```，DNS Servers填写```192.168.8.1```

## 设置DNS

1. 设置DNS缓存

    点击**IP**->**DNS**，Server填写```223.5.5.5```,```119.29.29.29```,```2400:3200::1```和```2402:4e00::```，勾选```Allow Remote Requests```。

2. 设置自动切换为旁路由dns

    点击**Tools**->**Netwatch**，点击+号，添加一个新的Netwatch Host。
    + 选择**Host**选项卡。Host填写```192.168.8.3```，Type选择```simple```。
    + 选择**Up**选项卡，设定IP上线时的操作(On Up)：

        ```ros
        /log info message="192.168.8.3 up!"
        /ip/firewall/mangle enable numbers=0
        /ip dns set servers 192.168.8.3
        /ip dns cache flush
        ```

    + 选择**Down**选项卡，设定IP下线时的操作(On Down)：

        ```ros
        /log info message="192.168.8.3 down!"
        /ip/firewall/mangle disable numbers=0
        /ip dns set servers 223.5.5.5,119.29.29.29,2400:3200::1,2402:4e00::
        /ip dns cache flush
        ```

## 设置IPv6

1. 点击**Interface**，选择**Interface**选项卡，查看已创建的PPPOE Client，记录下```Actual MTU```列中的实际MTU值，本文以```1492```为例。

2. 点击**IPv6**->**DHCP Client**，点击+号，添加一个DHCPv6 Client，选择**DHCP**选项卡，Interface选择已创建的PPPOE Client，Request勾选```prefix```，Pool name填写```pool-ipv6```，Pool Prefix Length填```60```（有些地方可能要填写56），**取消**勾选```Use Peer DNS```，**取消**勾选```Add Default Route```，然后点右边的**Apply**，如果Prefix正确的话会显示状态栏**Status:Bound**，如果不正确就换个值再尝试。

3. 给网桥接口分配公网IPv6地址：点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address，Address填写```::1/64```，From Pool选择```pool-ipv6```，Interface选择```bridge-lan```，勾选```Advertise```。

4. 给网桥接口分配私有IPv6地址：点击**IPv6**->**Address**,点击+号，添加一个Ipv6 Address，Address填写```fd08::1/64```，Interface选择```bridge-lan```，勾选```Advertise```。

5. 点击**IPv6**->**ND**，选择**Interface**选项卡，选择默认的all规则，点击**Disable**禁用。点击+号，添加新的ND，Interface选择```bridge-lan```，RA Interval填写```60-120```，MTU填写之前查到的实际MTU值```1492```，DNS Servers填写```fd08::1```。

6. 点击**IPv6**->**ND**，选择**Prefixes**选项卡，点击**Default**，Valid Lifetime设置为```1d 00:00:00```，Preferred Lifetime设置为```00:12:00```。

## 设置UPnP

1. 点击**IP**->**UPnp**，勾选```Enabled```、```Allow To Disable External Interface```、```Show Dummy Rule```

    点击Interfaces，创建一个Upnp，Interface选择WAN口(```ether2-wan```)，type选择```external```

    点击Interfaces，创建一个Upnp，Interface选择```bridge-lan```，type选择```internal```

## 安全设置

1. 关闭不必要的服务

    点击**IP**->**Services**，只留下winbox与www

2. 设置管理员密码

    点击**System**->**Users**，设置admin的密码

3. 升级固件

    点击**System**->**Packages**，点击**Check For Updates**查找更新，一般选择stable通道。
