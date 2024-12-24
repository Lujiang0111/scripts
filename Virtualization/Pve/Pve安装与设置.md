# Pve安装与设置

## 官方资料

+ 下载地址：<https://www.proxmox.com/en/downloads>
+ 官方文档：<https://pve.proxmox.com/pve-docs/>

## 全新安装

+ 使用[rufus](https://rufus.ie)制作启动U盘进行安装，此处选择的是8.2版本。
+ 默认管理网址：<https://ip:8006>
+ 默认用户名：root

## 更改语言

+ 登录界面可以直接选择语言。
+ 进入主页面后在右上角点击用户名切换语言。

## 使用ssh连接到pve

+ 关机：`poweroff`
+ 重启：`reboot`

## 设置http代理

如果pve主机本身无法联网但有联网需求，需要设置http代理

```shell
cat <<- EOF > /etc/profile.d/proxy.sh
export http_proxy="http://username:password@ip:port"
export https_proxy="http://username:password@ip:port"
export no_proxy="localhost,127.0.0.1,::1"
EOF

source /etc/profile
```

## 修改软件源

可选ustc软件源或无订阅软件源

### 屏蔽原有企业版软件源

```shell
sed -i 's/^/# /' /etc/apt/sources.list.d/pve-enterprise.list
```

### ustc软件源

> 参考资料：<https://mirrors.ustc.edu.cn/help/proxmox.html>

运行脚本（将`bookworm`修改为对应版本）

```shell
# 修改基础系统（Debian）的源文件
sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

# 修改 Proxmox 的源文件
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

# 修改 Ceph 的源文件
if [ -f /etc/apt/sources.list.d/ceph.list ]; then
  CEPH_CODENAME=`ceph -v | grep ceph | awk '{print $(NF-1)}'`
  source /etc/os-release
  echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/ceph-$CEPH_CODENAME $VERSION_CODENAME no-subscription" > /etc/apt/sources.list.d/ceph.list
fi
```

### 无订阅软件源

> 参考资料：<https://pve.proxmox.com/wiki/Package_Repositories>

+ 屏蔽原有企业版软件源

```shell
sed -i 's/^/# /' /etc/apt/sources.list.d/pve-enterprise.list
```

+ 添加无订阅存储库

```shell
nano /etc/apt/sources.list
```

修改为以下内容（把`bookworm`修改为对应版本）

```plain
deb http://ftp.debian.org/debian bookworm main contrib
deb http://ftp.debian.org/debian bookworm-updates main contrib

# Proxmox VE pve-no-subscription repository provided by proxmox.com,
# NOT recommended for production use
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription

# security updates
deb http://security.debian.org/debian-security bookworm-security main contrib
```

#### 修改Ceph软件源

```shell
nano /etc/apt/sources.list.d/ceph.list
```

修改为以下内容（把`bookworm`修改为对应版本）

```plain
# 注释掉原有企业源
# deb https://enterprise.proxmox.com/debian/ceph-quincy bookworm enterprise
# 添加无订阅软件源
deb http://download.proxmox.com/debian/ceph-reef bookworm no-subscription
```

### 更新软件源

```shell
apt update -y
apt full-upgrade -y
```

重启系统

```shell
reboot
```

## 安装vim

```shell
apt install -y vim
```

## 设置静态IPv6地址

+ 编辑网络配置文件

```shell
vim /etc/network/interfaces
```

+ 为网络接口配置IPv6地址 找到与你的网络接口（如`vmbr0`）相关的配置，然后添加或修改IPv6 配置。

```config
auto vmbr0
iface vmbr0 inet static
	address 192.168.8.6/24
	gateway 192.168.8.1
	bridge-ports enp8s0
	bridge-stp off
	bridge-fd 0

# IPv6 config
iface vmbr0 inet6 static
	address fd08::6/64
	gateway fd08::1
```

+ 重启网络服务

```shell
systemctl restart networking
```

## 去除未订阅提示

+ 使用ssh连接到pve
+ 编辑`proxmoxlib.js`文件

```shell
vim /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

+ 将`if (res === null || res === undefined || !res || res.data.status.toLowerCase() !== 'active')`判断改为`if (false)`

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

## 设置PCI直通

> 参考资料：<https://pve.proxmox.com/wiki/PCI(e)_Passthrough>

### 修改grub文件

+ 编辑`/etc/default/grub`文件
+ 修改`GRUB_CMDLINE_LINUX_DEFAULT`所在行内容为`GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"`

```shell
# check before
cat /etc/default/grub | grep GRUB_CMDLINE_LINUX_DEFAULT

sed -i '/^GRUB_CMDLINE_LINUX_DEFAULT/c\GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"' /etc/default/grub

#check after
cat /etc/default/grub | grep GRUB_CMDLINE_LINUX_DEFAULT
```

+ 更新grub

```shell
update-grub
reboot
```

### 添加Kernel Modules

+ 修改`/etc/modules`文件

```shell
# delete last blank line
sed -i '${/^$/d;}' /etc/modules

cat <<- EOF >> /etc/modules
vfio
vfio_iommu_type1
vfio_pci
EOF

#check after
cat /etc/modules
```

### 将显卡驱动加入黑名单

> 参考资料：<https://pve.proxmox.com/wiki/PCI_Passthrough>

+ AMD GPUs

```shell
echo "blacklist amdgpu" >> /etc/modprobe.d/blacklist.conf
echo "blacklist radeon" >> /etc/modprobe.d/blacklist.conf
```

+ NVIDIA GPUs

```shell
echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf
echo "blacklist nvidia*" >> /etc/modprobe.d/blacklist.conf
```

+ Intel GPUs(注意直通后可能导致vnc失效)

```shell
echo "blacklist i915" >> /etc/modprobe.d/blacklist.conf
```

### 应用更改

```shell
update-initramfs -u -k all
reboot
```

## 为虚拟机添加PCI设备

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
    + 标记该设备为虚拟机主显卡，勾选后虚拟机将会忽略配置中的`显示`选项。

  + PCI-Express (pcie=on|off)
    + 告诉 Proxmox VE 使用PCIe还是PCI端口。一些设备组合需要PCIe而非PCI。PCIe只在q35机型上有效。

  + ROM-Bar (rombar=on|off)
    + 使固件ROM对客户机可见。默认已勾选，有些PCI(e)设备需要禁用。

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
