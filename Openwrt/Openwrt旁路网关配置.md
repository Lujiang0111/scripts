# Openwrt旁路网关配置

## pve导入镜像

+ `img`镜像：

  ```shell
  qm importdisk 111 /var/lib/vz/template/iso/openwrt-x86-64-generic-squashfs-combined-efi.img local-lvm
  ```

+ `qcow2`镜像：

  ```shell
  qm importdisk 111 /root/openwrt-x86-64-generic-squashfs-combined-efi.qcow2 local-lvm
  ```

## 网络配置

- 系统 -> 系统
  - 设置时区
  - 设置NTP服务器地址。
- 系统 -> 管理权：
  - 设置密码
- 网络 -> 接口 -> LAN：
  - 基本设置
    - IPv4地址 - `192.168.8.11`
    - IPv4网关 - `192.168.8.1`
    - IPv4广播 - `192.168.8.255`
    - DNS服务器 - `223.5.5.5`
    - IPv6分配长度 - `64`
    - IPv6后缀 - `::11`
  - DHCP服务器：
    - 禁用v4和v6所有设置
  - 物理设置
    - 桥接接口 - ✔
    - 启用IGMP嗅探 - ✔
- 网络 -> 接口
  - IPv6 ULA前缀 - `fd08::/64`。
- 网络 -> 防火墙
  - 常规设置
    - 启用 SYN-flood 防御 - ❌
    - 入站数据、出站数据、转发 - `接受`
  - 区域
    - 全选择`接受`
    - lan => wan IP动态伪装 - ✔
