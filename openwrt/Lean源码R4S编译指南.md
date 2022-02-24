# Openwrt lean R4S 编译指南

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

### LuCI -> Applications

1. 勾选(y)luci-app-passwall
2. 勾选(y)luci-app-transmission

### LuCI -> Themes

1. 勾选(y)luci-theme-argon

### Utilities -> Disc

1. 勾选(y)fdisk
2. 勾选(y)parted

### Utilities -> Editors

1. 勾选(y)vim

## 开始编译

1. ```make -j8 download V=s``` 下载dl库（国内请尽量全局科学上网）
2. 若第一次执行有超时导致fail的情况，再次执行```make -j8 download V=s```
3. ```nohup make -j$(($(nproc) + 1)) V=s &```

## tips

1. 用ext4的Img不要用squashfs的img, 我不知道原因是什么，有可能是[#6956](https://github.com/coolsnowwolf/lede/issues/6956)的原因。

2. 如何刷固件:

    <https://yangc.yuque.com/books/share/8ee83942-8524-45ec-ae58-6b07d8bcfa1c/krqbh9>
