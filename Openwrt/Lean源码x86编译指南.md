# lean源码x86编译指南

## 编译步骤

1. 参考<https://github.com/coolsnowwolf/lede>,命令行输入```sudo apt-get update```，然后输入```sudo apt-get -y install build-essential asciidoc binutils bzip2 gawk gettext git libncurses5-dev libz-dev patch python3 python2.7 unzip zlib1g-dev lib32gcc1 libc6-dev-i386 subversion flex uglifyjs git-core gcc-multilib p7zip p7zip-full msmtp libssl-dev texinfo libglib2.0-dev xmlto qemu-utils upx libelf-dev autoconf automake libtool autopoint device-tree-compiler g++-multilib antlr3 gperf wget curl swig rsync```

2. 使用```git clone https://github.com/coolsnowwolf/lede```命令下载好源代码，然后```cd lede```进入目录

3. 添加额外源

    + <https://github.com/kenzok8/openwrt-packages>
    + <https://github.com/fw876/helloworld>

    ```bash
    sed -i '$a src-git kenzo https://github.com/kenzok8/openwrt-packages' feeds.conf.default
    sed -i '$a src-git small https://github.com/kenzok8/small' feeds.conf.default
    #sed -i '$a src-git helloworld https://github.com/fw876/helloworld.git' feeds.conf.default
    ```

4. 输入

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

1. ```make -j8 download V=s``` 下载dl库（国内请尽量全局科学上网）
2. ```nohup make -j$(($(nproc) + 1)) V=s &```
