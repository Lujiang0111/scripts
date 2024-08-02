# CentOS7更换Vault源

+ CentOS7已经在2024年6月30日结束生命周期，官方不再进行支持维护,如果使用官方yum源下载会报404。
+ 可以使用以下脚本(`centos7-change-vault.sh`)将默认源改为Vault源实现环境的安装。

```shell
#!/bin/bash

new_repo_url="https://mirror.moack.co.kr/.resource/CentOS-Base-7-Vault.repo"
old_repo_path="/etc/yum.repos.d/CentOS-Base.repo"

if [ "$(id -u)" != "0" ]; then
   echo "Error: This script needs to be run with root privileges" 1>&2
   exit 1
fi

echo -e "Backup old CentOS-Base.repo file..."
cp ${old_repo_path} "${old_repo_path}.bak"

echo -e "Downloading new CentOS-Base-7-Vault.repo file..."
curl -o ${old_repo_path} ${new_repo_url}

echo "updating yum cache..."
yum clean all
yum makecache
echo -e "Successfully replaced with CentOS Vault repository source"
```
