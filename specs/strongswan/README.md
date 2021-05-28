# Сборка STRONGSWAN

## Зависимости
```
yum install -y systemd-devel gmp-devel libcurl-devel openldap-devel openssl-devel sqlite-devel gettext-devel trousers-devel libxml2-devel pam-devel json-c-devel libgcrypt-devel iptables-devel NetworkManager-libnm-devel rpm-build
yum groupinstall -y 'Development Tools'
```
## Сборка
```
rpmbuild --undefine=_disable_source_fetch -ba strongswan.spec
```
