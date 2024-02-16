# Ros配置端口映射

## 明确映射信息

- 协议 - tcp
- 外网端口 - 56888
- 内网端口 - 6888
- 内网ip - 192.168.8.2

## IPv4

### 回流设置

- 请确认已经对内网接口做了masquerade(或无条件masquerade)，否则无法回流

```shell
/ip firewall nat add action=masquerade chain=srcnat comment="defconf: masquerade IPv4"
```

### 映射脚本

```shell
/ip/firewall/nat add chain=dstnat protocol=tcp dst-port=56888 dst-address-type=local action=dst-nat to-addresses=192.168.8.2 to-ports=6888 comment="forward aria2"
```

## IPv6

```shell
/ipv6/firewall/filter/add chain=forward protocol=tcp dst-port=6888 action=accept comment="allow aria2"
```

**注意**：添加规则后需要手动将规则移动至对应drop规则前面！
