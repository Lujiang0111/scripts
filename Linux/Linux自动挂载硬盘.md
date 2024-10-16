# Linux自动挂载硬盘

## 安装基础库

```shell
apt install btrfs-progs
```

## 确认硬盘信息

你可以使用以下命令列出所有硬盘和分区：

```shell
fdisk -l
```

确定系统中未使用的硬盘设备名称，例如`/dev/nvme0n1`。

## 创建btrfs分区

1. 如果该硬盘尚未分区，你可以使用`fdisk`或`parted`创建一个新的分区。以下是使用`fdisk`的步骤：

    ```shell
    fdisk /dev/nvme0n1
    ```

    在`fdisk`交互界面中：
    1. 输入`n`创建新分区。
    1. 选择分区号（通常选择默认即可）。
    1. 选择起始扇区和结束扇区（通常使用默认值以创建整个硬盘的分区）。
    1. 输入`w`写入分区表并退出。

1. 查看新分区的名称，例如`/dev/nvme0n1p1`。

    ```shell
    fdisk -l
    ```

1. 创建Btrfs文件系统

    ```shell
    mkfs.btrfs /dev/nvme0n1p1
    ```

## 获取分区的uuid

```shell
blkid /dev/nvme0n1p1
```

输出会类似于：

```shell
/dev/nvme0n1p1: UUID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" TYPE="btrfs"
```

这里的`UUID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`就是分区的 UUID。

## 配置挂载

### 新建挂载目的文件夹

```shell
mkdir -p /mnt/sn640
```

### 配置自动挂载

在`/etc/fstab`文件末尾添加需要挂载的硬盘：

```shell
cat <<- EOF >> /etc/fstab
# SN640
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /mnt/sn640 btrfs defaults 0 0
EOF
```

请将`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`替换为你实际的 UUID。

## 验证设置

你可以使用以下命令重新挂载所有在`/etc/fstab`中定义的文件系统，以验证配置是否正确：

```shell
systemctl daemon-reload
mount -a
```

如果没有任何错误提示，表示测试成功，重启系统。

```shell
reboot
```

重启后，使用`df -h`或`lsblk`命令检查挂载是否正常。
