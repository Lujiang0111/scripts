# Pve挂载新硬盘做储存

> 参考资料：<https://boonsoft.cn/?p=205>
> 参考资料：<https://csdaomin.com/2022/01/22/add-hard-drive-to-proxmox7>

## 新硬盘分区

1. 使用ssh连接到pve，查看系统中所有磁盘及其分区信息。

    ```shell
    fdisk -l
    ```

    ```shell
    root@pve245:~# fdisk -l
    Disk /dev/nvme0n1: 238.47 GiB, 256060514304 bytes, 500118192 sectors
    Disk model: INTEL SSDPEKKW256G8                     
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 1E7E2553-620F-422E-B717-331F1A2DE301

    Device           Start       End   Sectors   Size Type
    /dev/nvme0n1p1      34      2047      2014  1007K BIOS boot
    /dev/nvme0n1p2    2048   2099199   2097152     1G EFI System
    /dev/nvme0n1p3 2099200 500118158 498018959 237.5G Linux LVM


    Disk /dev/sda: 447.13 GiB, 480103981056 bytes, 937703088 sectors
    Disk model: KINGSTON SA400S3
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 162ECA87-44B3-4177-994B-EE8EA1C7D754
    ```

1. 针对磁盘准备进行操作，选择磁盘，进入磁盘工具。

    ```shell
    fdisk /dev/sda
    ```

1. 使用`d`删除已有分区，`n`创建新分区，修改完后使用`w`保存修改，重启系统。

    ```shell
    reboot
    ```

1. 重启后再次使用`fdisk`命令查看分区信息，发现分区成功了。

    ```shell
    root@pve245:~# fdisk -l
    Disk /dev/sda: 447.13 GiB, 480103981056 bytes, 937703088 sectors
    Disk model: KINGSTON SA400S3
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 162ECA87-44B3-4177-994B-EE8EA1C7D754

    Device     Start       End   Sectors   Size Type
    /dev/sda1   2048 937701375 937699328 447.1G Linux filesystem
    ```

1. 格式化分区为`ext4`格式。

    ```shell
    mkfs -t ext4 /dev/sda1
    ```

## 挂载分区

1. 将分区挂载到目录上

    ```shell
    mkdir -p /mnt/ssd
    mount -t ext4 /dev/sda1 /mnt/ssd
    ```

    但这种方式有个问题，就是重启的时候，label可能会改变。此时sda可能会变成sdb。所以如果在自动挂载的/etc/fstab脚本里，可以使用 uuid 。

1. 查看硬盘的uuid

    ```shell
    ls -al /dev/disk/by-uuid/
    ```

    ```shell
    root@pve245:~# ls -al /dev/disk/by-uuid/
    total 0
    drwxr-xr-x 2 root root 120 May 29 18:09 .
    drwxr-xr-x 7 root root 140 May 29 17:55 ..
    lrwxrwxrwx 1 root root  10 May 29 17:55 018b45f3-5dae-411f-ab00-38ed665aa229 -> ../../dm-0
    lrwxrwxrwx 1 root root  15 May 29 17:55 5492-D261 -> ../../nvme0n1p2
    lrwxrwxrwx 1 root root  10 May 29 18:09 54e35a42-c4b8-449f-8cb9-56f76594a3ad -> ../../sda1
    lrwxrwxrwx 1 root root  10 May 29 17:55 5ae2b027-d51f-4498-b665-f60e3da834c5 -> ../../dm-1
    ```

    由此可知硬盘`/dev/sda1`的UUID为`54e35a42-c4b8-449f-8cb9-56f76594a3ad`

1. 使用`fstab`进行自动挂载

    ```shell
    echo 'UUID=54e35a42-c4b8-449f-8cb9-56f76594a3ad /mnt/ssd ext4 defaults 0 1' >> /etc/fstab
    ```

1. 重启系统。

    ```shell
    reboot
    ```

## 在PVE的管理界面上添加硬盘

1. 点击**数据中心**->**存储**->**添加**->**目录**

    | 名称 | 设置值 |
    | - | - |
    | ID | ssd |
    | 目录 | /mnt/ssd |
    | 启用 | ✔ |
