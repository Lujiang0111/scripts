# Docker配置jellyfin服务器

> 参考资料：<https://hub.docker.com/r/nyanmisaka/jellyfin>

## 创建目录

```shell
# config dir
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

## 挂载SMB远端目录

### 安装`cifs-utils`软件包

```shell
apt install cifs-utils
```

### 测试挂载

```shell
# set your_username, your_password, //server/share
mkdir -p /mnt/smb/dsm/video
mount -t cifs -o username=your_username,password=your_password //server/share /mnt/smb/dsm/video
```

### 配置自动挂载

```shell
# set your_username, your_password, //server/share
cat <<- EOF >> /etc/fstab
# DSM video
//server/share /mnt/smb/dsm/video cifs x-systemd.automount,username=your_username,password=your_password 0 0
EOF
```

测试挂载

```shell
mount -a
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
      - /mnt/smb:/nas_smb
    ports:
      - 58096:8096
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```
