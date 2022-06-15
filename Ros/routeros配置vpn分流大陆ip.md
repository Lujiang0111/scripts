# ros配置vpn分流大陆ip

## 1. 生成ros大陆ip列表配置文件

使用[geolite2](https://github.com/firehol/blocklist-ipsets/tree/master/geolite2_country)生成

```bash
curl -s https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/geolite2_country/country_cn.netset \
| sed -e '/^#/d'\
| sed -e 's/^/add address=/g' -e 's/$/ list=CNIP/g' \
| sed -e $'1i\\\n/ip firewall address-list' -e $'1i\\\nremove [/ip firewall address-list find list=CNIP]' -e $'1i\\\nadd address=10.0.0.0/8 list=CNIP comment=private-network' -e $'1i\\\nadd address=172.16.0.0/12 list=CNIP comment=private-network' -e $'1i\\\nadd address=192.168.0.0/16 list=CNIP comment=private-network' \
> cnip.rsc
```

## 2. ros配置

1. winbox中上传cnip.rsc，使用```import cnip.rsc```导入配置文件。
2. 添加内网需要翻墙的ip列表。
3. 配置ip firewall的mangle
prerouting，source address list，destination address list取反，destination address type，address type local，invert，mark routing，cross-gfw。
配置ip routes的网关
0.0.0.0/0，gateway设置为vpn对端地址，routing mark 使用上面的cross-gfw。
