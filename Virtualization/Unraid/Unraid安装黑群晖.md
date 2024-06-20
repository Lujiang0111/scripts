# Unraid安装黑群晖

## 新建虚拟机

1. 新建黑群晖镜像存储文件夹`/mnt/user/domains/DSM`。
1. 下载[引导镜像](https://github.com/RROrg/rr/releases)，解压出img镜像，上传至镜像存储文件夹。
1. unraid中新建虚拟机，按下表所示设置
    | 名称 | 设置值 |
    | - | - |
    | 操作系统 | Linux |
    | CPU | 1/2/4/8个 |
    | 内存 | 4G以上 |
    | BIOS | OVMF |
    | Enable USB boot | Yes |
    | USB Controller | 3.0(qemu XHCI) |
    | Primary vDisk Location | Manual，路径手段选择`/mnt/user/domains/DSM/rr-24.6.5.img` |
    | Primary vDisk Bus | USB |
    | 2nd vDisk Location | Auto(默认是`/mnt/user/domains/Linux/vdisk2.img`) |
    | 2nd vDisk Type | qcow2 |
    | 2nd vDisk Bus | SATA |
    | Network Model | e1000 |
    | 直通 | 需要直通的设备 |

## 编译黑群晖引导文件

1. 根据虚拟机shell提示，访问<http://ip:7681>进入群晖安装画面。
1. 选择`Choose a model`，型号的选择参考<https://bbs.nga.cn/read.php?tid=38650456>，不使用硬解的话选择`DS3622xs+`。
1. 选择`Choose a version`，选择安装版本。
1. 复制pat的url，下载并保存，后续需要上传。
1. 选择`Build the loader`，开始编译黑群晖引导文件。
