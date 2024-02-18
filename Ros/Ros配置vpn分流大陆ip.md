# ros配置vpn分流大陆ip

> 参考资料：<https://www.willnet.net/index.php/archives/369/>

## 生成ros大陆ip列表脚本文件

+ 使用[geolite2](https://github.com/firehol/blocklist-ipsets/tree/master/geolite2_country)生成

```shell
curl -s https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/geolite2_country/country_cn.netset \
| sed -e '/^#/d'\
| sed -e 's/^/add address=/g' -e 's/$/ list=CNIP/g' \
| sed -e '1i/ip firewall address-list' -e '1iremove [/ip firewall address-list find list=CNIP]' -e '1iadd address=10.0.0.0/8 list=CNIP comment=private-network' -e '1iadd address=172.16.0.0/12 list=CNIP comment=private-network' -e '1iadd address=192.168.0.0/16 list=CNIP comment=private-network' \
> CNIP.rsc
```

+ 使用[chnroutes2](https://github.com/misakaio/chnroutes2)生成（更小巧，推荐）

```shell
curl -s https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt \
| sed -e '/^#/d'\
| sed -e 's/^/add address=/g' -e 's/$/ list=CNIP/g' \
| sed -e '1i/ip firewall address-list' -e '1iremove [/ip firewall address-list find list=CNIP]' -e '1iadd address=10.0.0.0/8 list=CNIP comment=private-network' -e '1iadd address=172.16.0.0/12 list=CNIP comment=private-network' -e '1iadd address=192.168.0.0/16 list=CNIP comment=private-network' \
> CNIP.rsc
```

## ros配置

假设**192.168.8.1**是ros的IP，**192.168.8.5**是旁路由的IP，其余IP是需要翻墙的内网ip。

### 导入大陆IP列表

winbox中点击**Files**->**Upload**上传cnip.rsc脚本文件。点击**New Terminal**打开控制台，在terminal中输入

```shell
import CNIP.rsc
```

导入脚本，此脚本会添加名称为```CNIP```的Address List。

### 配置需要翻墙的内网地址列表

点击**Ip**->**Firewall**，选择**Address Lists**标签，新建名称为```FQIP```的Address List，地址为需要翻墙的内网IP，可用脚本批量添加）。

+ 命令行方式为：

```shell
/ip firewall address-list
add address=192.168.8.2 list=FQIP
add address=192.168.8.3 list=FQIP
add address=192.168.8.4 list=FQIP
add address=192.168.8.6 list=FQIP
......
```

+ 脚本方式为：
  + Linux下编写名称为FQIP.sh的脚本文件

    ```shell
    #!/bin/bash
    fqip_file=FQIP.rsc

    cat <<- EOF > ${fqip_file}
    /ip firewall address-list
    remove [/ip firewall address-list find list=FQIP]
    EOF

    for ((i=2; i<=4; i++))
    do
        echo -e "add address=192.168.8.${i} list=FQIP" >> ${fqip_file}
    done

    for ((i=6; i<=239; i++))
    do
        echo -e "add address=192.168.8.${i} list=FQIP" >> ${fqip_file}
    done
    ```

  + Linux下运行FQIP.sh，生成FQIP.rsc

    ```shell
    bash FQIP.sh
    ```

  + ros下导入FQIP.rsc

    ```shell
    import FQIP.rsc
    ```

### 配置分流路由表

点击**Routing**->**Tables**，新建一个Routing Table，名称为```rtab-fq```，勾选```FIB```。

```shell
/routing/table/add name="rtab-fq" fib
```

### 添加IP分流策略路由

点击**Ip**->**Routes**，新建一个Route，Dst. Address填写```0.0.0.0/0```，Gateway填写```192.168.8.5```，Routing Table选择```rtab-fq```。

```shell
/ip/route/add dst-address=0.0.0.0/0 routing-table="rtab-fq" gateway=192.168.8.5 check-gateway=ping
```

### 给需要翻墙的内网ip添加标记

+ 点击**Ip**->**Firewall**，选择**Mangle**标签，新建一个Mangle Rule。

+ 选择Gereral标签，Chain选择```prerouting```，Src. Address List选择```FQIP```，Dst. Address List选择```CNIP```，勾选```CNIP```前面的感叹号（取反）。

+ 选择Extra标签，Dst. Address Type选择```local```，勾选```local```前面的感叹号（取反）。

+ 选择Action标签，Action选择```mark routing```，取消勾选Log，New Routing Make选择```rtab-fq```，勾选```Passthrough```。

+ 将词条Mangle规则移至fasttrack后面（number=3）。

```shell
/ip/firewall/mangle/add chain=prerouting action=mark-routing new-routing-mark=rtab-fq passthrough=yes dst-address-type=!local src-address-list=FQIP dst-address-list=!CNIP log=no place-before=3
```

### 设置Netwatch，根据旁路由启停状况自动切换配置

+ 点击**Tools**->**Netwatch**，点击+号，添加一个新的Netwatch Host。
  + 选择**Host**选项卡。Host填写```192.168.8.5```，Type选择```icmp```。
  + 选择**Up**选项卡，设定IP上线时的操作(On Up)：

    ```shell
    /log info message="192.168.8.5 up!"
    /ip/firewall/mangle/enable numbers=3
    /ip dns set servers 192.168.8.5
    /ip dns cache flush
    ```

  + 选择**Down**选项卡，设定IP下线时的操作(On Down)：

    ```shell
    /log info message="192.168.8.5 down!"
    /ip/firewall/mangle/disable numbers=3
    /ip dns set servers 223.5.5.5,119.29.29.29
    /ip dns cache flush
    ```

### 修改Ros默认防火墙（ROS初始配置已包含）

+ 打开 **IP** > **Firewall** > **Filter Rules**，找到 `action=drop chain=forward comment="drop invalid" connection-state=invalid` 这一条，将**General**下的**In. Interface List**改为`!LAN`防止防火墙将加密过后的流量标记为invalid而造成TCP流量握手缓慢。

+ 打开 **IP** > **Firewall** > **Filter Rules**，找到`defconf: fasttrack`这一条, 将**General**下的**In. Interface List**设置为`WAN`，防止Fasttrack与Mangle冲突。
