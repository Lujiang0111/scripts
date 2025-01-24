# Docker配置aria2_pro服务器

> 参考资料：<https://github.com/P3TERX/Aria2-Pro-Docker>

## 创建目录

```shell
# config dir
rm -rf /opt/docker/aria2-pro/config
mkdir -p /opt/docker/aria2-pro/config
chmod 777 /opt/docker/aria2-pro/config

# data dir
mkdir -p /mnt/ssd/download/aria2
chmod 777 /mnt/ssd/download/aria2
```

## 配置docker容器

+ `docker_compose.yml`

```yml
services:
  aria2-Pro:
    container_name: aria2-pro
    image: p3terx/aria2-pro:latest
    environment:
      - PUID=1000
      - PGID=1000
      - UMASK_SET=022
      - RPC_SECRET=your_secret # set your_secret
      - RPC_PORT=56800
      - LISTEN_PORT=56888
      - DISK_CACHE=64M
      - IPV6_MODE=true
      - UPDATE_TRACKERS=true
      - TZ=Asia/Shanghai
    volumes:
      - /opt/docker/aria2-pro/config:/config
      - /mnt/ssd/download/aria2:/downloads
    networks:
      macvlan_enp6s18:
        ipv4_address: 192.168.8.43
        ipv6_address: fd08::43
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: 1m
networks:
  macvlan_enp6s18:
    external: true
```
