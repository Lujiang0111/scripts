# ROS配置防火墙使内网用户直接访问光猫

> 参考链接：<https://www.ioiox.com/archives/111.html>

## 简介

为方便下文理解,示例如下:

+ 请自行根据实际情况修改下文命令参数中的IP网段
  + ```192.168.100.1/24```为光猫IP及网段。
  + ```192.168.8.1/24```为路由IP及网段。
+ 本教程并不适合光猫与主路由在同一网段的场景。

## ROS设置

### 在光猫网段添加WAN口IP

+ 点击**IP**->**Address**，添加一个WAN口IP。注意WAN口IP和光猫需在同一网段,例如```192.168.100.2```。
  + **Address** - ```192.168.100.2/24```
  + **Interface** - ```WAN```

### 设置防火墙

+ 点击**IP**->**Firewall**，选择**NAT**选项卡，添加一条NAT规则。
  + **General**
    + **Chain** - ```srcnat```
    + **Src. Address** - ```192.168.8.0/24```
    + **Dst. Address** - ```192.168.100.0/24```
  + **Action**
    + **Action** - ```masquerade```

+ 点击**IP**->**Firewall**，选择**Mangle**选项卡，添加一条Mangle规则。
  + **General**
    + **Chain** - ```prerouting```
    + **Src. Address** - ```192.168.8.0/24```
    + **Dst. Address** - ```192.168.100.0/24```
  + **Action**
    + **Action** - ```accept```

## 访问光猫

浏览器输入光猫内网IP即可访问管理页面。
