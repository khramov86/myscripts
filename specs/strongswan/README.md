# Сборка STRONGSWAN

## Зависимости
```
yum install -y wget systemd-devel gmp-devel libcurl-devel openldap-devel openssl-devel sqlite-devel gettext-devel trousers-devel libxml2-devel pam-devel json-c-devel libgcrypt-devel iptables-devel NetworkManager-libnm-devel rpm-build
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
```
linux_ver=5.10.42
strongswan_ver=5.9.2
patch_ver=5.10
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-${linux_ver}.tar.xz
xz -d linux-${linux_ver}.tar.xz && tar xf linux-${linux_ver}.tar
rm -f linux-{linux_ver}.tar
wget https://download.strongswan.org/testing/ha-${patch_ver}-abicompat.patch.bz2
bzip2 -d ha-${patch_ver}-abicompat.patch.bz2
pushd linux-5.10.42
patch -p1 < ../ha-${patch_ver}-abicompat.patch
popd
wget https://download.strongswan.org/strongswan-${strongswan_ver}.tar.gz
tar xzf strongswan-${strongswan_ver}.tar.gz
rm -f strongswan-${strongswan_ver}.tar.gz
cd strongswan-${strongswan_ver}
. /opt/rh/devtoolset-9/enable
./configure --disable-static --sysconfdir=/etc/strongswan --enable-ha --bindir=/usr/bin/ --with-linux-headers=/root/linux-${linux_ver}/
make -j $(nproc)
make install
```

### Подготовка к сборке

`make defconfig` - подготовить дефолтный конфиг `.config`

`make menuconfig` - конфигурировать через утилиту ncurses

### Сборка ядра
```
make bzImage -j $(nproc)
make modules -j $(nproc)
make -j $(nproc)
make modules_install
make install
```
## Сборка
```
rpmbuild --undefine=_disable_source_fetch -ba strongswan.spec

```

