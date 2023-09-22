# lean源码编译指南

## 编译步骤

> 参考资料：<https://github.com/coolsnowwolf/lede>

1. 首先装好Linux 系统，推荐Debian 11或Ubuntu LTS。

2. 安装编译依赖

    ```shell
    sudo clear
    ```

    ```shell
    sudo apt update -y
    ```

    ```shell
    sudo apt full-upgrade -y
    ```

    ```shell
    sudo apt install -y ack antlr3 asciidoc autoconf automake autopoint binutils bison build-essential \
    bzip2 ccache cmake cpio curl device-tree-compiler fastjar flex gawk gettext gcc-multilib g++-multilib \
    git gperf haveged help2man intltool libc6-dev-i386 libelf-dev libglib2.0-dev libgmp3-dev libltdl-dev \
    libmpc-dev libmpfr-dev libncurses5-dev libncursesw5-dev libreadline-dev libssl-dev libtool lrzsz \
    mkisofs msmtp nano ninja-build p7zip p7zip-full patch pkgconf python2.7 python3 python3-pyelftools \
    libpython3-dev qemu-utils rsync scons squashfs-tools subversion swig texinfo uglifyjs upx-ucl unzip \
    vim wget xmlto xxd zlib1g-dev python3-setuptools
    ```

3. 下载源代码

    ```shell
    git clone https://github.com/coolsnowwolf/lede
    cd lede
    ```

4. 添加额外源

    1. 整合版
        + <https://github.com/kenzok8/openwrt-packages>

        ```shell
        cat <<- EOF >> feeds.conf.default
        src-git kenzo https://github.com/kenzok8/openwrt-packages
        src-git small https://github.com/kenzok8/small
        EOF
        ```

    2. ssrp
        + <https://github.com/fw876/helloworld>

        ```shell
        cat <<- EOF >> feeds.conf.default
        src-git helloworld https://github.com/fw876/helloworld.git
        EOF
        ```

    3. passwall
        + <https://github.com/xiaorouji/openwrt-passwall>

        ```shell
        cat <<- EOF >> feeds.conf.default
        src-git passwall_packages https://github.com/xiaorouji/openwrt-passwall.git;packages
        src-git passwall_luci https://github.com/xiaorouji/openwrt-passwall.git;luci
        EOF
        ```

    4. openclash
        + <https://github.com/vernesong/OpenClash>

        ```shell
        cat <<- EOF >> feeds.conf.default
        src-git openclash https://github.com/vernesong/OpenClash.git
        EOF
        ```

    5. 自用源
        + <https://github.com/Lujiang0111/openwrt-packages>

        ```shell
        sed -i '1 i src-git lujiang0111 https://github.com/Lujiang0111/openwrt-packages.git' feeds.conf.default
        ```

5. 更新feeds

    ```shell
    ./scripts/feeds update -a
    ./scripts/feeds install -a
    ```

## 添加自定义包

+ [mosdns](https://github.com/sbwml/luci-app-mosdns)

    ```shell
    # drop mosdns and v2ray-geodata packages that come with the source
    find ./ | grep Makefile | grep v2ray-geodata | xargs rm -f
    find ./ | grep Makefile | grep mosdns | xargs rm -f

    git clone https://github.com/sbwml/luci-app-mosdns -b v5 package/mosdns
    git clone https://github.com/sbwml/v2ray-geodata package/v2ray-geodata
    ```

+ [luci-theme-argon](https://github.com/jerrykuku/luci-theme-argon)

    ```shell
    cd package/lean
    rm -rf luci-theme-argon
    git clone https://github.com/jerrykuku/luci-theme-argon.git -b 18.06 luci-theme-argon
    cd -
    ```

+ [luci-app-argon-config](https://github.com/jerrykuku/luci-app-argon-config)

    ```shell
    cd feeds/luci/applications
    rm -rf luci-app-argon-config
    git clone https://github.com/jerrykuku/luci-app-argon-config.git -b 18.06 luci-app-argon-config
    cd -
    ```

+ [smartdns](https://github.com/pymumu/luci-app-smartdns)

    ```shell
    WORKINGDIR="`pwd`/feeds/packages/net/smartdns"
    mkdir $WORKINGDIR -p
    rm $WORKINGDIR/* -fr
    wget https://github.com/pymumu/openwrt-smartdns/archive/master.zip -O $WORKINGDIR/master.zip
    unzip $WORKINGDIR/master.zip -d $WORKINGDIR
    mv $WORKINGDIR/openwrt-smartdns-master/* $WORKINGDIR/
    rmdir $WORKINGDIR/openwrt-smartdns-master
    rm $WORKINGDIR/master.zip

    LUCIBRANCH="lede"
    WORKINGDIR="`pwd`/feeds/luci/applications/luci-app-smartdns"
    mkdir $WORKINGDIR -p
    rm $WORKINGDIR/* -fr
    wget https://github.com/pymumu/luci-app-smartdns/archive/${LUCIBRANCH}.zip -O $WORKINGDIR/${LUCIBRANCH}.zip
    unzip $WORKINGDIR/${LUCIBRANCH}.zip -d $WORKINGDIR
    mv $WORKINGDIR/luci-app-smartdns-${LUCIBRANCH}/* $WORKINGDIR/
    rmdir $WORKINGDIR/luci-app-smartdns-${LUCIBRANCH}
    rm $WORKINGDIR/${LUCIBRANCH}.zip

    ./scripts/feeds update -a
    ./scripts/feeds install -a
    ```

## 修改具体配置

1. 修改内核版本

    ```shell
    vim target/linux/x86/Makefile
    ```

    修改```KERNEL_PATCHVER:```为自己所需要的内核版本：

    ```makefile
    # 修改为5.4内核
    KERNEL_PATCHVER:=5.4
    ```

2. 修改LAN口IP设置

    ```shell
    vim package/base-files/files/bin/config_generate
    ```

    修改LAN口ip```192.168.1.1```为自己所需要的：

    ```shell
    lan) ipad=${ipaddr:-"192.168.1.1"} ;;
    ```

3. 开启ssr-plus的insecure选项

    ```shell
    vim feeds/helloworld/luci-app-ssr-plus/root/usr/share/shadowsocksr/subscribe.lua
    ```

    修改processData函数Trojan分支的result.insecure选项为```1```

    ```lua
    -- 将下方result.insecure的值修改为1

    -- 按照官方的建议 默认验证ssl证书
    result.insecure = "0"
    ```

4. 修改passwall的启动延时

    ```shell
    vim feeds/passwall_luci/luci-app-passwall/root/usr/share/passwall/0_default_config
    ```

    将```option start_delay```的值从60修改为```5```

    ```lua
    option start_delay '5'
    ```

## 编译选项

```shell
make menuconfig
```

### Target Images

1. Root filesystem partition size改为合适大小

### Extra packages

1. 取消(n)```automount```

### Base system

1. 取消(n)```block-mount```

### LuCI -> Applications

1. 可**取消**勾选(n)```luci-app-accesscontrol```，```luci-app-adbyby-plus```，```luci-app-ddns```，```luci-app-ipsec-vpnd```，```luci-app-turboacc```，```luci-app-unblockmusic```，```luci-app-upnp```，```luci-app-wireguard```，```luci-app-wol```，```luci-app-xlnetacc```，```luci-app-zerotier```。
2. 编译ssrp时，如果需要IPv6解析，需要取消勾选(n)```ChinaDNS-NG```。

### LuCI -> Themes

1. 勾选(y)```luci-theme-argon-mod```

### Utilities -> Editors

1. 勾选(y)```vim```

## 无线网卡相关配置

### Kernel modules -> Wireless Drivers

1. 勾选(y)```kmod-mt76x2u``` *(NETGEAR A6210)*
2. 勾选(y)```kmod-rtl8821cu``` *(COMFAST CF-811AC)*

### Network -> WirelessAPD

1. 勾选(y)```hostapd```

## 开始编译

1. 下载dl库

    ```shell
    make -j$(nproc) download V=s
    ```

2. 编译固件

    ```shell
    nohup make -j$(nproc) V=s &
    ```

## 旁路网关设置说明

1. 网络 -> 接口 -> LAN，**保持**桥接，设置IPv4地址，子网掩码，网关，广播（```.255```)，DNS服务器（```223.5.5.5```），IPv6前缀（```::5```），**关闭**DHCP服务。

2. 网络 -> 接口，IPv6 ULA前缀填写```fd08::/64```。

3. 网络 -> 防火墙，**取消**“启用 SYN-flood 防御”，**勾选**LAN区域的“IP动态伪装”。
