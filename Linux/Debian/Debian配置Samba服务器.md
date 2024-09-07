# Debian配置Samba服务器

## 安装Samba

```shell
apt install samba
```

## 创建共享目录

```shell
mkdir -p /mnt/sn640/fastshare
chmod 777 /mnt/sn640/fastshare
```

## 配置Samba

```shell
vim /etc/samba/smb.conf
```

在文件中添加如下内容：

```conf
[ShareName]
   path = /srv/samba/share
   browseable = yes
   writable = yes
   guest ok = yes
   read only = no

```