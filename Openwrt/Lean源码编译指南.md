# lean源码编译指南

## 编译步骤

> 参考资料：<https://github.com/coolsnowwolf/lede>

1. 首先装好Linux 系统，推荐Debian 11或Ubuntu LTS。

2. 安装编译依赖

    ```bash
    sudo clear
    ```

    ```bash
    sudo apt update -y
    ```

    ```bash
    sudo apt full-upgrade -y
    ```

    ```bash
    sudo apt install -y ack antlr3 aria2 asciidoc autoconf automake autopoint binutils bison build-essential \
    bzip2 ccache cmake cpio curl device-tree-compiler fastjar flex gawk gettext gcc-multilib g++-multilib \
    git gperf haveged help2man intltool libc6-dev-i386 libelf-dev libglib2.0-dev libgmp3-dev libltdl-dev \
    libmpc-dev libmpfr-dev libncurses5-dev libncursesw5-dev libreadline-dev libssl-dev libtool lrzsz \
    mkisofs msmtp nano ninja-build p7zip p7zip-full patch pkgconf python2.7 python3 python3-pip libpython3-dev qemu-utils \
    rsync scons squashfs-tools subversion swig texinfo uglifyjs upx-ucl unzip vim wget xmlto xxd zlib1g-dev
    ```

3. 下载源代码

    ```bash
    git clone https://github.com/coolsnowwolf/lede
    cd lede
    ```

4. 添加额外源

    1. 整合版
        + <https://github.com/kenzok8/openwrt-packages>

        ```bash
        cat <<- EOF >> feeds.conf.default
        src-git kenzo https://github.com/kenzok8/openwrt-packages
        src-git small https://github.com/kenzok8/small
        EOF
        ```

    2. ssrp独立版
        + <https://github.com/fw876/helloworld>

        ```bash
        sed -i '$a src-git helloworld https://github.com/fw876/helloworld.git' feeds.conf.default
        ```

    3. passwall独立版
        + <https://github.com/xiaorouji/openwrt-passwall>

        ```bash
        cat <<- EOF >> feeds.conf.default
        src-git passwall_packages https://github.com/xiaorouji/openwrt-passwall.git;packages
        src-git passwall_luci https://github.com/xiaorouji/openwrt-passwall.git;luci
        EOF
        ```

    4. 自用源

        ```bash
        sed -i '$a src-git lujiang0111 https://github.com/Lujiang0111/openwrt-packages-feed.git' feeds.conf.default
        ```

5. 更新feeds并选择配置

    ```bash
    ./scripts/feeds update -a
    ./scripts/feeds install -a
    make menuconfig
    ```

## 编译选项

### Target Images

1. Root filesystem partition size改为合适大小

### Extra packages

1. 取消(n)automount

### LuCI -> Applications

1. 勾选相应插件

### LuCI -> Themes

1. 勾选(y)luci-theme-argon

### Utilities -> Editors

1. 勾选(y)vim

## 无线网卡相关配置

### Kernel modules -> Wireless Drivers

1. 勾选(y)kmod-mt76x2u *(NETGEAR A6210)*
2. 勾选(y)kmod-rtl8821cu *(COMFAST CF-811AC)*

### Network -> WirelessAPD

1. 勾选(y)hostapd

## 开始编译

1. 修改默认设置

    ```bash
    vim package/base-files/files/bin/config_generate
    ```

    修改默认ip```192.168.1.1```为自己所需要的：

    ```bash
    lan) ipad=${ipaddr:-"192.168.1.1"} ;;
    ```

2. 下载dl库

    ```bash
    make -j$(nproc) download V=s
    ```

3. 编译固件

    ```bash
    nohup make -j$(nproc) V=s &
    ```

## 旁路网关设置说明

1. 网络 -> 接口 -> LAN，如果LAN只有一个网口，则取消桥接；如果LAN有多个网口或者包含wifi，则保持桥接。

2. 网络 -> 接口 -> LAN，设置IPv4地址，子网掩码，网关，广播（.255)，DNS服务器（223.5.5.5），**关闭**DHCP服务。

3. 网络 -> 防火墙，**取消**“启用 SYN-flood 防御”，**勾选**LAN区域的“IP动态伪装”。
