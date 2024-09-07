# Docker配置samba服务器

> 参考资料：<https://github.com/ServerContainers/samba/tree/master>

## 创建需要共享的目录

```shell
mkdir -p /mnt/sn640/fastshare
chmod -R 0777 /mnt/sn640/fastshare
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
      ACCOUNT_lujiang: ices0081234
      UID_lujiang: 1000
      SAMBA_VOLUME_CONFIG_fastshare: >
        [fastshare]; path=/shares/fastshare;
        guest ok = no; read only = no; browseable = yes;
        create mask = 0664; directory mask = 0775
    volumes:
      - /mnt/sn640/fastshare:/shares/fastshare
    ports:
      - 445:445
```
