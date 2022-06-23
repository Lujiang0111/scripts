# Openwrt lean R4S 编译指南

## 编译步骤

> 参考资料：<https://github.com/coolsnowwolf/lede>

1. 首先装好Linux 系统，推荐Debian 11或Ubuntu LTS。

2. 安装编译依赖

    ```bash
    sudo apt update -y
    sudo apt full-upgrade -y
    sudo apt install -y ack antlr3 asciidoc autoconf automake autopoint binutils bison build-essential \
    bzip2 ccache cmake cpio curl device-tree-compiler fastjar flex gawk gettext gcc-multilib g++-multilib \
    git gperf haveged help2man intltool libc6-dev-i386 libelf-dev libglib2.0-dev libgmp3-dev libltdl-dev \
    libmpc-dev libmpfr-dev libncurses5-dev libncursesw5-dev libreadline-dev libssl-dev libtool lrzsz \
    mkisofs msmtp nano ninja-build p7zip p7zip-full patch pkgconf python2.7 python3 python3-pip qemu-utils \
    rsync scons squashfs-tools subversion swig texinfo uglifyjs upx-ucl unzip vim wget xmlto xxd zlib1g-dev
    ```

3. 下载源代码

    ```bash
    git clone https://github.com/coolsnowwolf/lede
    cd lede
    ```

4. 添加额外源

    + <https://github.com/kenzok8/openwrt-packages>
    + <https://github.com/fw876/helloworld>

    ```bash
    sed -i '$a src-git kenzo https://github.com/kenzok8/openwrt-packages' feeds.conf.default
    sed -i '$a src-git small https://github.com/kenzok8/small' feeds.conf.default
    #sed -i '$a src-git helloworld https://github.com/fw876/helloworld.git' feeds.conf.default
    ```

5. 更新feeds并选择配置

    ```bash
    ./scripts/feeds update -a
    ./scripts/feeds install -a
    make menuconfig
    ```

## 编译选项

### Target System

1. 勾选(y)Rockchip

### Target Profile

1. 勾选(y)FriendlyARM NanoPi R4S

### Target Images

1. Kernel partition size改为64
2. Root filesystem partition size改为512

### Global build settings

1. 取消(n)Enable IPv6 support in packages

### Kernel modules -> Wireless Drivers

1. 勾选(y)kmod-mt76x2u *(NETGEAR A6210)*
2. 勾选(y)kmod-rtl8821cu *(COMFAST CF-811AC)*

### LuCI -> Applications

1. 勾选(y)luci-app-passwall *(如果添加了kenzok8源）*

### LuCI -> Themes

1. 勾选(y)luci-theme-argon

### Network -> WirelessAPD

1. 勾选(y)hostapd
2. 勾选(y)wpa-supplicant

### Utilities -> Editors

1. 勾选(y)vim

## 开始编译

1. 下载dl库，编译固件(国内尽量全局科学上网)

    ```bash
    make -j$(nproc) download V=s
    nohup make -j$($(nproc)) V=s &
    ```

## 旁路网关设置说明

1. 网络 -> 接口 -> LAN，**保持桥接**，设置IPv4地址，子网掩码，网关，广播（.255)，DNS服务器（223.5.5.5），**关闭**DHCP服务。
2. 网络 -> 防火墙，**取消**“启用 SYN-flood 防御”，**勾选**LAN区域的“IP动态伪装”。

## tips

1. 用ext4的Img不要用squashfs的img, 我不知道原因是什么，有可能是[#6956](https://github.com/coolsnowwolf/lede/issues/6956)的原因。

2. 如何刷固件:

    <https://yangc.yuque.com/books/share/8ee83942-8524-45ec-ae58-6b07d8bcfa1c/krqbh9>
