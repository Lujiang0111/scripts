# centos7 默认防火墙firewalld配置

> 参考资料：<https://www.cnblogs.com/hubing/p/6058932.html>

## 控制firewalld启停

+ 启动：```systemctl start  firewalld```
+ 状态：```systemctl status firewalld```或者```firewall-cmd --state```
+ 停止：```systemctl disable firewalld```
+ 禁用：```systemctl stop firewalld```

## 查看default zone和active zone

我们还没有做任何配置，default zone和active zone都应该是public。

```bash
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones
```

## 查看当前启用了那些服务（端口）

一个服务对应一系列端口，每个服务对应```/usr/lib/firewalld/services```下面一个xml文件。

```bash
firewall-cmd --list-services
```

## 更新防火墙规则

```bash
firewall-cmd --reload
```

## 启用一个服务

```bash
firewall-cmd --permanent --add-service=http #http换成想要开放的service
```

```--permanent```代表永久启用

## 添加自定义服务并启用

1. 在```/usr/lib/firewalld/services```目录下新建一个xml文件，如test.xml。
2. 修改test.xml为如下格式

    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <service>
        <short>test</short>
        <description>test service file</description>

        <!-- rtsp -->
        <port protocol="tcp" port="554" />
        <port protocol="udp" port="554" />

        <!-- dash -->
        <port protocol="tcp" port="1901" />

        <!-- rtmp -->
        <port protocol="tcp" port="1935" />

        <!-- httpflv -->
        <port protocol="tcp" port="1936" />

        <!-- hls -->
        <port protocol="tcp" port="8888" />

        <!-- udp list -->
        <port protocol="udp" port="18800-30000" />
    </service>
    ```

3. 启用该服务```firewall-cmd --permanent --add-service=test```
