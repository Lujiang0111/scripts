# ImmortalWrt源码编译指南

> 参考资料：<https://github.com/immortalwrt/immortalwrt>

## 安装依赖

+ 首先装好Linux系统，推荐Ubuntu LTS。

+ 安装编译依赖

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
bzip2 ccache clang cmake cpio curl device-tree-compiler ecj fastjar flex gawk gettext gcc-multilib \
g++-multilib git gnutls-dev gperf haveged help2man intltool lib32gcc-s1 libc6-dev-i386 libelf-dev \
libglib2.0-dev libgmp3-dev libltdl-dev libmpc-dev libmpfr-dev libncurses5-dev libncursesw5 \
libncursesw5-dev libpython3-dev libreadline-dev libssl-dev libtool lld llvm lrzsz mkisofs msmtp \
nano ninja-build p7zip p7zip-full patch pkgconf python2.7 python3 python3-pip python3-ply \
python-docutils python3-pyelftools qemu-utils re2c rsync scons squashfs-tools subversion swig \
texinfo uglifyjs upx-ucl unzip vim wget xmlto xxd zlib1g-dev
```

## 下载源码

+ 下载源代码

```shell
git clone -b openwrt-21.02 --depth=1 https://github.com/immortalwrt/immortalwrt.git
cd immortalwrt
```

+ 更新feeds

```shell
./scripts/feeds update -a
./scripts/feeds install -a
```

## 添加自定义包

+ [openclash](https://github.com/vernesong/OpenClash)

```shell
git clone -b dev --depth=1 https://github.com/vernesong/OpenClash.git
rm feeds/luci/applications/luci-app-openclash/ -rf
mv OpenClash/luci-app-openclash feeds/luci/applications/
rm OpenClash/ -rf
```

+ [uu加速器](http://router.uu.163.com/api/plugin?type=openwrt-x86_64)
  + 修改相应的版本号和PKG_HASH值([SHA256](https://emn178.github.io/online-tools/sha256_checksum.html))

```shell
vim feeds/packages/net/uugamebooster/Makefile
```

## 修改配置

+ 修改LAN口IP设置

```shell
vim package/base-files/files/bin/config_generate
```

修改LAN口ip```192.168.1.1```为自己所需要的：

```shell
lan) ipad=${ipaddr:-"192.168.1.1"} ;;
```

## 编译选项

```shell
./scripts/feeds install -a
make menuconfig
```

### Target Images

+ Root filesystem partition size改为合适大小

### Global build settings

+ 取消勾选(```n```)**Enable IPv6 support in packages**

### Extra packages

+ 取消(n)```automount```

### Base system

+ 取消(n)```block-mount```

### LuCI -> Applications

+ 选择```luci-app-argon-config```、```luci-app-aria2```、```luci-app-openclash```、```luci-app-udpxy```、```luci-app-uugamebooster```、```luci-app-vlmcsd```等插件

### Network -> SSH

1. 勾选(y)```openssh-sftp-server```。

## 开始编译

+ 下载dl库

```shell
make -j$(nproc) download V=s
```

+ 编译固件

```shell
nohup make -j$(nproc) V=s &
```
