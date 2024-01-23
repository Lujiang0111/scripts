# Pve安装img镜像虚拟机

## 上传img镜像

+ pve页面选择：数据中心 -> pve -> local(pve) -> ISO镜像 -> 上传，选择img镜像上传。

## 将镜像导入虚拟机中

+ ssh连接pve，执行下列命令将这个img镜像导入到虚拟机中
  + 100为虚拟机的ID, 替换为实际ID。
  + local-lvm是存储的名字，替换为实际储存。

```shell
qm importdisk 100 /var/lib/vz/template/iso/openwrt.img local-lvm
```

+ 之后就可以在虚拟机中看到这个未使用的磁盘。编辑这个磁盘，不用改动，点**编辑**->**添加**即可。

## 修改引导顺序

+ 修改虚拟机的引导顺序，在虚拟机的**选项**->**引导顺序**中，勾选刚才的磁盘。
