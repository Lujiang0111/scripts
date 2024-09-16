# Docker配置samba服务器

> 参考资料：<https://github.com/ServerContainers/samba/tree/master>

## 创建需要共享的目录

```shell
# data dir
mkdir -p /mnt/sn640/fastshare
chmod 777 /mnt/sn640/fastshare
mkdir -p /mnt/sn640/download
chmod 777 /mnt/sn640/download
mkdir -p /mnt/sn640/xvideos
chmod 777 /mnt/sn640/xvideos
mkdir -p /mnt/sn640/storage
chmod 777 /mnt/sn640/storage
```

## 配置docker容器

+ `docker_compose.yml`

```yml
version: "3.8"
services:
  samba:
    restart: unless-stopped
    image: ghcr.io/servercontainers/samba:latest
    container_name: samba
    cap_add:
      - CAP_NET_ADMIN
    environment:
      ACCOUNT_lujiang: your_password # set your_password
      UID_lujiang: 1000
      SAMBA_VOLUME_CONFIG_fastshare: >
        [fastshare]; path=/shares/fastshare;
        guest ok = no; read only = no; browseable = yes;
        create mask = 0664; directory mask = 0775
      SAMBA_VOLUME_CONFIG_download: >
        [download]; path=/shares/download;
        guest ok = no; read only = no; browseable = yes;
        create mask = 0664; directory mask = 0775
      SAMBA_VOLUME_CONFIG_xvideos: >
        [xvideos]; path=/shares/xvideos;
        guest ok = no; read only = no; browseable = yes;
        create mask = 0664; directory mask = 0775
      SAMBA_VOLUME_CONFIG_storage: >
        [storage]; path=/shares/storage;
        guest ok = no; read only = no; browseable = yes;
        create mask = 0664; directory mask = 0775
    volumes:
      - /mnt/sn640/fastshare:/shares/fastshare
      - /mnt/sn640/download:/shares/download
      - /mnt/sn640/xvideos:/shares/xvideos
      - /mnt/sn640/storage:/shares/storage
    ports:
      - 445:445
```
