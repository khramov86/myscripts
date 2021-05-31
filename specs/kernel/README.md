# Kernel build instructions

```
yum install libmpc-devel mpfr-devel 
yum group install "Development Tools"
yum install ncurses-devel bison flex elfutils-libelf-devel openssl-devel bzip2
rpm -Uvh https://ftp.yandex.ru/centos/7.9.2009/os/x86_64/Packages/libmpc-devel-1.0.1-3.el7.x86_64.rpm
cd /root
curl ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/releases/gcc-4.9.2/gcc-4.9.2.tar.bz2 -O
tar xvfj gcc-4.9.2.tar.bz2
cd gcc-4.9.2
./configure --disable-multilib --enable-languages=c,c++
make -j $(nproc)
```
можно указывать конкретное количество ядер через -j 4

make install


https://www.cyberciti.biz/tips/compiling-linux-kernel-26.html


## Обновление ядра
https://www.howtoforge.com/tutorial/how-to-upgrade-kernel-in-centos-7-server



## Альтернативная установка GCC
```
yum install centos-release-scl-rh
yum install devtoolset-3-gcc devtoolset-3-gcc-c++
update-alternatives --install /usr/bin/gcc-4.9 gcc-4.9 /opt/rh/devtoolset-3/root/usr/bin/gcc 10
update-alternatives --install /usr/bin/g++-4.9 g++-4.9 /opt/rh/devtoolset-3/root/usr/bin/g++ 10
```

```
yum install scl-utils
```

## Сборка ядра
Дополнительные зависимости
```
rpm -Uvh http://mirror.centos.org/centos/7/extras/x86_64/Packages/centos-release-scl-rh-2-3.el7.centos.noarch.rpm
rpm -Uvh http://mirror.centos.org/centos/7/extras/x86_64/Packages/centos-release-scl-2-3.el7.centos.noarch.rpm
```
Можно взять конфигурацию у текущего ядра
```
cp -v /boot/config-$(uname -r) .config
```
Порядок сборки
```
make menuconfig
make bzImage
make modules
make
make modules_install
make install
```
## Выбор другого ядра для загрузки

Посмотреть список ядре
```
awk -F\' '$1=="menuentry " {print i++ " : " $2}' /etc/grub2.cfg
```
Установка ядра для загрузки
```
grub2-set-default 0
grub2-mkconfig -o /boot/grub2/grub.cfg
```

## Уменьшение размера ядра


## Уменьшение размера ядра


In `/etc/initramfs-tools/initramfs.conf`, set `MODULES=dep` instead of `MODULES=most`. The initrd build process will work out what modules you need rather than including a wide variety of things. Note, however, that this makes your boot process very dependent on your hardware and if you need to use a different set of hardware (in particular, drives) the initrd may not work.

Additionally you can choose a better compression algorithm, the default should still be gzip, but xz (or lzma2) is also available via `COMPRESS=xz`. Of course you need to have xz-utils installed. The initial compression takes longer, but decompression during boot shouldn't take much longer. Both options together may also reduce your boot time a little bit.

After setting this, run `sudo update-initramfs -u -k all` to have it take effect.

