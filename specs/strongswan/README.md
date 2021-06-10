# Сборка STRONGSWAN

## Зависимости
```
yum install -y systemd-devel gmp-devel libcurl-devel openldap-devel openssl-devel sqlite-devel gettext-devel trousers-devel libxml2-devel pam-devel json-c-devel libgcrypt-devel iptables-devel NetworkManager-libnm-devel rpm-build
yum groupinstall -y 'Development Tools'
```
## Сборка с kernel-include
Добавить в файл `/etc/yum.repos.d/CentOS-SCLo-scl.repo`:
```
# CentOS-SCLo-sclo.repo
#
# Please see http://wiki.centos.org/SpecialInterestGroup/SCLo for more
# information

[centos-sclo-sclo]
name=CentOS-7 - SCLo sclo
baseurl=http://mirror.centos.org/centos/7/sclo/$basearch/rh
#mirrorlist=http://mirrorlist.centos.org?arch=$basearch&release=7&repo=sclo-sclo
gpgcheck=0
enabled=1

[centos-sclo-sclo-testing]
name=CentOS-7 - SCLo sclo Testing
baseurl=http://buildlogs.centos.org/centos/7/sclo/$basearch/rh
gpgcheck=0
enabled=0

[centos-sclo-sclo-source]
name=CentOS-7 - SCLo sclo Sources
baseurl=http://vault.centos.org/centos/7/sclo/Source/sclo/
gpgcheck=0
enabled=1


[centos-sclo-sclo-debuginfo]
name=CentOS-7 - SCLo sclo Debuginfo
baseurl=http://debuginfo.centos.org/centos/7/sclo/$basearch/
gpgcheck=0
enabled=1
```
Устанавливаем свежую версию gcc
```
yum install devtoolset-9 -y
```

## Сборка
```
rpmbuild --undefine=_disable_source_fetch -ba strongswan.spec
```

