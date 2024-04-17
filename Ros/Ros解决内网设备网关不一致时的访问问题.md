# Ros解决内网设备网关不一致时的访问问题

## 问题描述

| 名称 | IP | 网关 |
| - | - | - |
| Ros bridge-lan | 192.168.8.1 | |
| 旁路网关 | 192.168.8.5 | 192.168.8.1 |
| 内网设备 | 192.168.8.22 | 192.168.8.5 |
| Ros Wireguard服务端 | 192.168.9.1 |  |
| 远程 Wireguard客户端 | 192.168.9.2 | 192.168.9.1 |

此时使用Wireguard客户端`192.168.9.2`ping内网设备`192.168.8.22`时无法ping通。

## 解决方案

## 方案1：使用分流大陆ip时配置的Routing Table

```shell
/ip/firewall/mangle/add chain=prerouting in-interface=wireguard-lan dst-address=192.168.8.22 action=mark-routing new-routing-mark=rtab-fq passthrough=yes comment="routing wireguard to 192.168.8.22"
```

## 方案2：添加静态路由

添加静态路由，目的地址`192.168.8.22`，网关`192.168.8.5`。

```shell
/ip/route/add dst-address=192.168.8.22 gateway=192.168.8.5 comment="routing to 192.168.8.22"
```
