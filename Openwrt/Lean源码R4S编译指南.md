# Openwrt lean R4S 编译指南

## 编译步骤

1. 参考<https://github.com/coolsnowwolf/lede>,命令行输入```sudo apt-get update```，然后输入```sudo apt-get -y install build-essential asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch python3 python2.7 unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake libtool autopoint device-tree-compiler g++-multilib antlr3 gperf wget curl swig rsync```

2. 使用```git clone https://github.com/coolsnowwolf/lede```命令下载好源代码，然后```cd lede```进入目录

3. 添加额外源

    + <https://github.com/kenzok8/openwrt-packages>
    + <https://github.com/fw876/helloworld>

    ```bash
    #sed -i '$a src-git kenzo https://github.com/kenzok8/openwrt-packages' feeds.conf.default
    #sed -i '$a src-git small https://github.com/kenzok8/small' feeds.conf.default
    sed -i '$a src-git helloworld https://github.com/fw876/helloworld.git' feeds.conf.default
    git pull
    ```

4. 输入

    ```bash
    ./scripts/feeds update -a
    ./scripts/feeds install -a
    make menuconfig
    ```

## 编译选项

### Target System

勾选(y)Rockchip

### Target Profile

勾选(y)FriendlyARM NanoPi R4S

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

1. ```make -j8 download V=s``` 下载dl库（国内请尽量全局科学上网）
2. 若第一次执行有超时导致fail的情况，再次执行```make -j8 download V=s```
3. ```nohup make -j$(($(nproc) + 1)) V=s &```

## 旁路网关设置说明

1. 网络 -> 接口 -> LAN，**保持桥接**，设置IPv4地址，子网掩码，网关，广播（.255)，DNS服务器（223.5.5.5），**关闭**DHCP服务。
2. 网络 -> 防火墙，**取消**“启用 SYN-flood 防御”，**勾选**LAN区域的“IP动态伪装”。

## tips

1. 用ext4的Img不要用squashfs的img, 我不知道原因是什么，有可能是[#6956](https://github.com/coolsnowwolf/lede/issues/6956)的原因。

2. 如何刷固件:

    <https://yangc.yuque.com/books/share/8ee83942-8524-45ec-ae58-6b07d8bcfa1c/krqbh9>
