# lean源码x86编译指南

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

### Target Images

1. Kernel partition size改为64
2. Root filesystem partition size改为512

### Global build settings

1. 取消(n)Enable IPv6 support in packages

### LuCI -> Applications

1. 勾选(y)luci-app-passwall *(如果添加了kenzok8源）*

### LuCI -> Themes

1. 勾选(y)luci-theme-argon

### Utilities -> Editors

1. 勾选(y)vim

## 开始编译

1. 下载dl库，编译固件(国内尽量全局科学上网)

    ```bash
    make -j8 download V=s
    nohup make -j$(($(nproc) + 1)) V=s &
    ```
