# Docker容器配置独立IP

## 创建macvlan网络

1. 查看网络接口

    ```shell
    ip a
    ```

    这里假设是`eth0`。

1. 创建IPv4和IPv6双栈的macvlan网络

    假设创建的macvlan接口为`macvlan_eth0`

    ```shell
    docker network create -d macvlan \
        --subnet=192.168.8.0/24 \
        --gateway=192.168.8.1 \
        --ipv6 \
        --subnet=fd08::/64 \
        --gateway=fd08::1 \
        -o parent=eth0 \
        macvlan_eth0
    ```

## docker run形式指定IP地址

```shell
docker run -d \
    --name=subconverter \
    --restart=always \
    --net=macvlan_eth0 \
    --ip=192.168.8.42 \
    --ip6=fd08::42 \
    -p 25500:25500 \
    tindy2013/subconverter:latest
```

## docker compose形式指定IP地址

```yml
version: "3.8"
services:
  subconverter:
    restart: always
    image: tindy2013/subconverter:latest
    ports:
      - 25500:25500
    networks:
      macvlan_eth0:
        ipv4_address: 192.168.8.42
        ipv6_address: fd08::42
networks:
  macvlan_eth0:
    external: true
```
