# Ubuntu启用root用户ssh登录

## 启用root用户

```bash
sudo passwd root
```

## 开启ssh的root登录权限

```bash
sudo vim /etc/ssh/sshd_config
```

找到配置参数：```PermitRootLogin```，将该参数后面的值修改为```yes```即可。

## 重启ssh服务

```bash
sudo systemctl restart ssh
```
