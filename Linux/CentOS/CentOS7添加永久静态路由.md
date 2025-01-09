# CentOS7添加永久静态路由

1. 在`/etc/sysconfig/network-scripts/`目录下创建一个路由配置文件，通常以 `route-<interface>`命名。例如接口是`eth0`，则创建`route-eth0`文件：

    ```shell
    vim /etc/sysconfig/network-scripts/route-eth0
    ```

1. 在文件中添加永久路由:

    ```shell
    192.168.2.0/24 via 192.168.1.1 dev eth0
    ```

1. 重启网络服务：

    ```shell
    systemctl restart network
    ```

    或重启

    ```shell
    reboot
    ```
