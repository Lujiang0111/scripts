# Pve安装与设置

## 官方资料

+ 下载地址：<https://www.proxmox.com/en/downloads>
+ 官方文档：<https://pve.proxmox.com/pve-docs/>

## 全新安装

+ 使用[rufus](https://rufus.ie)制作启动U盘进行安装，此处选择的是8.1版本。
  + 踩坑：制作完镜像后，直接拔出u盘，不要点弹出。
  + 踩坑：如果中途取消安装，再次安装前，需要清除U盘分区，重新用rufus制作镜像，否则会安装失败。
+ 默认管理网址：<https://ip:8006>
+ 默认用户名：root

## 更改语言

+ 登录界面可以直接选择语言。
+ 进入主页面后在右上角点击用户名切换语言。

## 使用ssh连接到pve

+ 关机：```poweroff```
+ 重启：```reboot```

## 去除未订阅提示

+ 使用ssh连接到pve
+ 编辑```proxmoxlib.js```文件

```shell
nano /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

+ 将```if (res === null || res === undefined || !res || res.data.status.toLowerCase() !== 'active')```判断改为```if (false)```

```js
if (false) {
    Ext.Msg.show({
        title: gettext('No valid subscription'),
        icon: Ext.Msg.WARNING,
        message: Proxmox.Utils.getNoSubKeyHtml(res.data.url),
        buttons: Ext.Msg.OK,
        callback: function(btn) {
            if (btn !== 'ok') {
                return;
            }
            orig_cmd();
        },
    });
} else {
    orig_cmd();
}
```

+ 执行

```shell
systemctl restart pveproxy
```

或重启

```shell
reboot
```

生效。

## 替换软件源为国内源

> 参考资料：<https://mirrors.ustc.edu.cn/help/proxmox.html>

+ 备份源文件

```shell
mkdir /etc/apt/sources_backup
cp /etc/apt/sources.list /etc/apt/sources_backup/sources.list.bak
cp /etc/apt/sources.list.d/ceph.list /etc/apt/sources_backup/ceph.list.bak
cp /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources_backup/pve-enterprise.list.bak
```

+ 将```/etc/apt/sources.list.d/pve-enterprise.list```文件清空

```shell
echo "" > /etc/apt/sources.list.d/pve-enterprise.list
```

+ 一般情况下，需要同时修改基础系统（Debian）的源文件 /etc/apt/sources.list 和 Proxmox 的源文件。

+ 修改基础系统（Debian）的源文件，可以使用如下命令：

```shell
sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list
```

+ 修改 Proxmox 的源文件，可以使用如下命令（可选，不太稳定）：

```shell
source /etc/os-release
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve $VERSION_CODENAME pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```

+ PVE 8 之后默认安装 ceph 仓库源文件 /etc/apt/sources.list.d/ceph.list，可以使用如下命令更换源：

```shell
if [ -f /etc/apt/sources.list.d/ceph.list ]; then CEPH_CODENAME=`ceph -v | grep ceph | awk '{print $(NF-1)}'`; source /etc/os-release; echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/ceph-$CEPH_CODENAME $VERSION_CODENAME no-subscription" > /etc/apt/sources.list.d/ceph.list; fi
```

+ CT Templates源替换（可选，升级pve版本后需要重新设置）

```shell
cp /usr/share/perl5/PVE/APLInfo.pm /usr/share/perl5/PVE/APLInfo.pm_back
sed -i 's|http://download.proxmox.com|https://mirrors.ustc.edu.cn/proxmox|g' /usr/share/perl5/PVE/APLInfo.pm
```

+ 替换后操作

```shell
apt update -y
apt full-upgrade -y
reboot
```

## 设置NTP时钟同步

> 参考资料：<https://pve.proxmox.com/wiki/Time_Synchronization>

+ 修改```/etc/chrony/chrony.conf```文件

```shell
nano /etc/chrony/chrony.conf
```

用```#```注释掉原有的```pool 2.debian.pool.ntp.org iburst```，在这行下面添加自定义NTP服务器

```conf
server cn.ntp.org.cn iburst
server cn.pool.ntp.org iburst
server ntp.aliyun.com iburst
server ntp.tencent.com iburst
```

+ 重启chrony服务

```shell
systemctl restart chronyd
```

## 设置PCI直通

### 修改grub文件

+ 修改```/etc/default/grub```文件

```shell
nano /etc/default/grub
```

+ 找到```GRUB_CMDLINE_LINUX_DEFAULT```行，Intel CPU添加```intel_iommu=on```，AMD CPU应该默认就有

+ ```GRUB_CMDLINE_LINUX_DEFAULT```添加```iommu=pt```

```ini
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
```

+ 更新grub并重启

```shell
update-grub
reboot
```

### 添加Kernel Modules

+ 修改```/etc/modules```文件

```shell
nano /etc/modules
```

+ 添加以下几行

```shell
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd # not needed if on kernel 6.2 or newer
```

+ 应用更改

```shell
update-initramfs -u -k all
reboot
```

### 为虚拟机添加PCI设备

+ **注意：不要将控制口的网卡给直通了！！**

+ 查看网卡pci地址:

```shell
ethtool -i enp87s0
```

```shell
driver: igc
version: 6.5.11-7-pve
firmware-version: 1057:8754
expansion-rom-version: 
# bus-info即pci地址
bus-info: 0000:57:00.0
supports-statistics: yes
supports-test: yes
supports-eeprom-access: yes
supports-register-dump: yes
supports-priv-flags: yes
```

+ 点击：虚拟机->硬件->添加->PCI设备
  + 所有功能
    + 如果该设备具有多个功能（例如显卡 01:00.0 和 01:00.1），勾选此选项会一起传递。

  + 主 GPU (x-vga=on|off)
    + 标记该设备为虚拟机主显卡，勾选后虚拟机将会忽略配置中的 显示 选项。

  + PCI-Express (pcie=on|off)
    + 告诉 Proxmox VE 使用 PCIe 还是 PCI 端口。一些设备组合需要 PCIe 而非 PCI。PCIe 只在 q35 机型上有效。

  + ROM-Bar (rombar=on|off)
    + 使固件 ROM 对客户机可见。默认已勾选，有些 PCI(e) 设备需要禁用。

## 设置PVE防火墙

> 参考资料：<https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pve_firewall>

### 设置数据中心防火墙

+ **注意**：如果启用防火墙，默认情况下会阻止到所有主机的流量。唯一的例外是本地网络中的WebGUI(8006)和 ssh(22)。

+ 数据中心 - 防火墙 - 添加
  + 添加自定义防火墙

+ 数据中心 - 防火墙 - 选项 - 启用

### 启用节点防火墙

+ 默认情况下节点防火墙是启用的。

+ 数据中心 - pve节点 - 防火墙 - 选项 - 启用

## 设置vm防火墙

+ 数据中心 - 节点 - vm - 防火墙 - 添加
  + 添加自定义防火墙

+ 数据中心 - 节点 - vm - 防火墙 - 选项 - 启用
