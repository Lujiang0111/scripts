# Docker配置Jellyfin服务器

> 参考资料：<https://hub.docker.com/r/nyanmisaka/jellyfin>

## 创建目录

```shell
rm -rf /opt/docker/jellyfin/config
mkdir -p /opt/docker/jellyfin/config
chmod 777 /opt/docker/jellyfin/config
rm -rf /opt/docker/jellyfin/cache
mkdir -p /opt/docker/jellyfin/cache
chmod 777 /opt/docker/jellyfin/cache
rm -rf /opt/docker/jellyfin/media
mkdir -p /opt/docker/jellyfin/media
chmod 777 /opt/docker/jellyfin/media
```

## 配置docker容器

+ `docker_compose.yml`

```yaml
version: "3.8"
services:
  jellyfin:
    restart: unless-stopped
    image: nyanmisaka/jellyfin:latest
    container_name: jellyfin
    environment:
      - TZ=Asia/Shanghai
      - NVIDIA_DRIVER_CAPABILITIES=all
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - /opt/docker/jellyfin/config:/config
      - /opt/docker/jellyfin/cache:/cache
      - /opt/docker/jellyfin/media:/media
      - /mnt/sn640/download:/nas_download
    ports:
      - 58096:8096
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```
