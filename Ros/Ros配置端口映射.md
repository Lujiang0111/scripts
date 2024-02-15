# Ros配置端口映射

## 明确映射信息

- 协议 - tcp
- 外网端口 - 56888
- 内网端口 - 6888
- 内网ip - 192.168.8.2

## 设置脚本

```shell
/ip/firewall/nat add chain=dstnat protocol=tcp dst-port=56888 in-interface-list=WAN action=dst-nat to-addresses=192.168.8.2 to-ports=6888
```
