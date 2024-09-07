# Debian安装N卡环境

## 安装Cuda和Nvida驱动

> 参考资料：<https://developer.nvidia.com/cuda-downloads>

完全按照参考资料的步骤执行，请以参考资料为准

+ CUDA Toolkit Installer

```shell
wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb
dpkg -i cuda-keyring_1.1-1_all.deb
apt -y update
apt -y install cuda-toolkit-12-6
```

+ Driver Installer

```shell
apt -y install nvidia-open
```

安装完成后重启系统

```shell
reboot
```

## 禁止内核更新

1. 查看当前内核版本

    ```shell
    uname -r
    dpkg --list | grep linux-image
    ```

    找到类似于`linux-image-X.X.X`的包名。

2. 锁定内核包

    ```shell
    sudo apt-mark hold linux-image-X.X.X
    ```

## 验证驱动安装

```shell
nvidia-smi
```

如果正确安装，应该会显示当前的显卡信息和驱动版本。
