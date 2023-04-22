# ros配置vpn分流大陆ip

> 参考资料：<https://www.willnet.net/index.php/archives/369/>

## 1. 生成ros大陆ip列表脚本文件

+ 使用[geolite2](https://github.com/firehol/blocklist-ipsets/tree/master/geolite2_country)生成

    ```bash
    curl -s https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/geolite2_country/country_cn.netset \
    | sed -e '/^#/d'\
    | sed -e 's/^/add address=/g' -e 's/$/ list=CNIP/g' \
    | sed -e '1i/ip firewall address-list' -e '1iremove [/ip firewall address-list find list=CNIP]' -e '1iadd address=10.0.0.0/8 list=CNIP comment=private-network' -e '1iadd address=172.16.0.0/12 list=CNIP comment=private-network' -e '1iadd address=192.168.0.0/16 list=CNIP comment=private-network' \
    > CNIP.rsc
    ```

+ 使用[chnroutes2](https://github.com/misakaio/chnroutes2)生成（更小巧，推荐）

    ```bash
    curl -s https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt \
    | sed -e '/^#/d'\
    | sed -e 's/^/add address=/g' -e 's/$/ list=CNIP/g' \
    | sed -e '1i/ip firewall address-list' -e '1iremove [/ip firewall address-list find list=CNIP]' -e '1iadd address=10.0.0.0/8 list=CNIP comment=private-network' -e '1iadd address=172.16.0.0/12 list=CNIP comment=private-network' -e '1iadd address=192.168.0.0/16 list=CNIP comment=private-network' \
    > CNIP.rsc
    ```

## 2. ros配置

+ 假设**192.168.8.1**是ros的IP，**192.168.8.5**是旁路由的IP，其余IP是需要翻墙的内网ip。

1. 导入大陆IP列表。

    winbox中点击**Files**->**Upload...**上传cnip.rsc脚本文件。点击**New Terminal**打开控制台，在terminal中输入

    ```ros
    import CNIP.rsc
    ```

    导入脚本，此脚本会添加名称为```CNIP```的Address List。

2. 配置需要翻墙的内网地址列表。

    点击**Ip**->**Firewall**，选择**Address Lists**标签，新建名称为```FQIP```的Address List，地址为需要翻墙的内网IP，可用脚本批量添加）。

    + 命令行方式为：

        ```ros
        /ip firewall address-list
        add address=192.168.8.2 list=FQIP
        add address=192.168.8.3 list=FQIP
        add address=192.168.8.4 list=FQIP
        add address=192.168.8.6 list=FQIP
        ......
        ```

    + 脚本方式为：

    1. Linux下编写名称为FQIP.sh的脚本文件

        ```bash
        #!/bin/bash
        fqip_file=FQIP.rsc

        cat <<- EOF > ${fqip_file}
        /ip firewall address-list
        remove [/ip firewall address-list find list=FQIP]
        add address=192.168.8.2 list=FQIP
        add address=192.168.8.3 list=FQIP
        add address=192.168.8.4 list=FQIP
        EOF

        for ((i=6; i<=239; i++))
        do
            echo -e "add address=192.168.8.${i} list=FQIP" >> ${fqip_file}
        done
        ```

    2. Linux下运行FQIP.sh，生成FQIP.rsc

        ```bash
        bash FQIP.sh
        ```

    3. ros下导入FQIP.rsc

        ```bash
        import FQIP.rsc
        ```

3. 配置分流路由表。

    点击**Routing**->**Tables**，新建一个Routing Table，名称为```rtab-fq```，勾选```FIB```。

    命令行方式为

    ```ros
    /routing/table/add name="rtab-fq" fib
    ```

4. 添加IP分流策略路由。

    点击**Ip**->**Routes**，新建一个Route，Dst. Address填写```0.0.0.0/0```，Gateway填写```192.168.8.5```，Routing Table选择```rtab-fq```，Check Gateway选择```arp```。

    命令行方式为

    ```ros
    /ip/route/add dst-address=0.0.0.0/0 routing-table="rtab-fq" gateway=192.168.8.5 check-gateway=arp
    ```

5. 给需要翻墙的内网ip添加标记。

    点击**Ip**->**Firewall**，选择**Mangle**标签，新建一个Mangle Rule。

    选择Gereral标签，Chain选择```prerouting```，Src. Address List选择```FQIP```，Dst. Address List选择```CNIP```，勾选```CNIP```前面的感叹号（取反）。

    选择Extra标签，Dst. Address Type选择```local```，勾选```local```前面的感叹号（取反）。

    选择Action标签，Action选择```mark routing```，取消勾选Log，New Routing Make选择```rtab-fq```，勾选```Passthrough```。

    命令行方式为

    ```ros
    /ip/firewall/mangle/add chain=prerouting action=mark-routing new-routing-mark=rtab-fq passthrough=yes dst-address-type=!local src-address-list=FQIP dst-address-list=!CNIP log=no log-prefix=""
    ```
