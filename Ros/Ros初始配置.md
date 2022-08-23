# Ros初始配置

## 设置网口与LAN IP

1. 确定WAN口与LAN口。

    打开winbox，使用MAC地址方式连接至ros。

    点击**Interface**，选择**Interface**选项卡，确定WAN口、2.5G口、SFP口等。修改Name为**ether1-2.5g**、**ether2-wan**等，方便记忆。

2. 设置LAN网桥。

    点击**Bridge**，选择**Bridge**选项卡，创建一个Interface。Name填写**lan-bridge**。

    选择**Ports**选项卡，创建New Bridge Port，Interface依次选择LAN网口，Bridge选择**lan-bridge**，有多少个LAN口就要创建多少个bridge。

3. 设置LAN IP。

    点击**IP**->**Addresses**，创建一个Address。Address填写想要分配的LAN IP**192.168.8.1/24**，Interface选择**lan-bridge**，设置完成后winbox就可以使用ip登录了。

## 设置拨号上网

1. 拨号上网设置。

    点击**Interface**，选择**Interface**选项卡，点击+号，选择**PPPOE Client**。选择General选项卡，Interfaces选择**WAN口**；选择Dial Out选项卡，User和Password填写拨号的用户名和密码，勾选**Add Default Route**

2. 设置IP伪装

    点击**IP**->**Firewall**，选择**MAT**选项卡，添加一条NAT规则。选择General选项卡，Chain选择**srcnat**；选择Action选项卡，Action选择**masquerade**，取消勾选Log。

## 设置DHCP

1. 设置DHCP IP池。

    点击**IP**->**Pool**，选择**Pools**选项卡，创建一个IP Pool。Name填写**dhcp-pool**，Addresses填写想要分配的地址池**192.168.8.20-192.168.8.240**，Next Pool选择none。

2. 设置DHCP

    点击**IP**->**DHCP Server**，选择**DHCP**选项卡，创建一个DHCP SERVER。选择General选项卡，Name填写**dhcp-server**，Interface选择**lan-bridge**，Address Pool选择**dhcp-pool**。

    选择**Networks**选项卡，新建一个DHCP Newwork。Address填写**192.168.8.0/24**，Gateway填写**192.168.8.1**，DNS Servers填写**192.168.8.1**

## 设置DNS

1. 设置DNS缓存

    点击**IP**->**DNS**，Server填写**223.5.5.5**和**119.29.29.29**，勾选**Allow Remote Requests**。

## 设置自动切换旁路由dns

1. 点击**System**->**Scripts**，选择**Scripts**选项卡，添加**startup-setdns-script**脚本。

    ```ros
    :global dnscheck false
    /log info message="dns first set to 223.5.5.5!";
    /ip dns set servers 223.5.5.5,119.29.29.29;
    /ip dns cache flush
    ```

2. 点击**System**->**Scripts**，选择**Scripts**选项卡，添加**change-dns-script**脚本。

    ```ros
    :global dnscheck
    :local curcheck ([:ping 192.168.8.3 count=5 interval=100ms]>3)
    :if ($curcheck && !$dnscheck) do={
        :log info message="dns change to 192.168.8.3!";
        :set dnscheck true;
        :ip dns set servers 192.168.8.3;
        :ip dns cache flush}
    :if (!$curcheck && $dnscheck) do={
        :log info message="dns change to 223.5.5.5!";
        :set dnscheck false;
        :ip dns set servers 223.5.5.5,119.29.29.29;
        :ip dns cache flush}
    ```

3. 点击**System**->**Scheduler**，创建一个Schedule，Name填写**startup-setdns-schedule**，Start Time选择**startup**，Interval填写**00:00:00**（不循环），On Event填写：

    ```ros
    :execute script="startup-setdns-script"
    ```

4. 点击**System**->**Scheduler**，创建一个Schedule，Name填写**change-dns-schedule**，Start Time选择**startup**，Interval填写**00:01:00**，On Event填写：

    ```ros
    :execute script="change-dns-script"
    ```

## 设置UPnP

1. 点击**IP**->**UPnp**，勾选**Enabled**、**Allow To Disable External Interface**、**Show Dummy Rule**

    点击Interfaces，创建一个Upnp，Interface选择**WAN口**，type选择**external**

    点击Interfaces，创建一个Upnp，Interface选择**lan-bridge**，type选择**internal**

## 安全设置

1. 关闭不必要的服务

    点击**IP**->**Services**，只留下winbox与www

2. 设置管理员密码

    点击**System**->**Users**，设置admin的密码

3. 升级固件

    点击**System**->**Packages**，点击**Check For Updates**查找更新，一般选择stable通道。
