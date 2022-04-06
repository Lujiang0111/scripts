# linux网络优化

## 1. 设置系统缓冲区大小

1. 查看当前缓冲区大小：

    ```bash
    cat /proc/sys/net/core/rmem_max
    cat /proc/sys/net/core/wmem_max
    ```

2. 打开配置文件：```sudo vim /etc/sysctl.conf```
3. 在文件末尾添加：

    ```bash
    net.core.rmem_max = 33554432
    net.core.wmem_max = 33554432
    ```

4. 执行配置：```sysctl -p```

## 2. 设置万兆网卡ring buffer

1. 查看当前网卡ring buffer size :

    ```bash
    :~ # ethtool -g eth1
    Ring parameters for eth1:
    Pre-set maximums:
    RX:             4096
    RX Mini:        0
    RX Jumbo:       0
    TX:             4096
    Current hardware settings:
    RX:             256
    RX Mini:        0
    RX Jumbo:       0
    TX:             256
    ```

    如上是确认网卡eth1的ring buffer size，输出结果中上面是预设的最大值，下面是当前设定值。
2. 临时调整Ring Buffer size: ```ethtool -G eth1 rx 4096 tx 4096```
3. 长久化修改Ring Buffer size

    上面的设定方法在reboot后就失效了，为了将这种修改恒久化，可以修改配置文件。

    ```bash
    $ vim /etc/rc.d/rc.local

    #!/bin/sh
    ethtool -G eth1 rx 4096 tx 4096
    ```

    修改完成后执行```sysctl -p```应用修改
