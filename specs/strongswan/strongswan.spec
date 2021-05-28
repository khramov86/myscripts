%global _hardened_build 1
#%%define prerelease dr1
%undefine _disable_source_fetch 

Name:           strongswan
Version:        5.9.2
Release:        1%{?dist}
Summary:        An OpenSource IPsec-based VPN and TNC solution
License:        GPLv2+
URL:            http://www.strongswan.org/
Source0:        http://download.strongswan.org/%{name}-%{version}%{?prerelease}.tar.bz2
# Source0:	https://github.com/strongswan/strongswan/archive/%{version}.tar.gz

# only needed for pre-release versions
#BuildRequires:  autoconf automake

BuildRequires:  systemd-devel
BuildRequires:  gmp-devel
BuildRequires:  libcurl-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel
BuildRequires:  gettext-devel
BuildRequires:  trousers-devel
BuildRequires:  libxml2-devel
BuildRequires:  pam-devel
BuildRequires:  json-c-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  systemd-devel
BuildRequires:  iptables-devel

BuildRequires:  NetworkManager-libnm-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The strongSwan IPsec implementation supports both the IKEv1 and IKEv2 key
exchange protocols in conjunction with the native NETKEY IPsec stack of the
Linux kernel.

%package libipsec
Summary: Strongswan's libipsec backend
%description libipsec
The kernel-libipsec plugin provides an IPsec backend that works entirely
in userland, using TUN devices and its own IPsec implementation libipsec.

%package charon-nm
Summary:        NetworkManager plugin for Strongswan
Requires:       dbus
Obsoletes:      %{name}-NetworkManager < 0:5.0.4-5
Conflicts:      %{name}-NetworkManager < 0:5.0.4-5
Conflicts:      NetworkManager-strongswan < 1.4.2-1
%description charon-nm
NetworkManager plugin integrates a subset of Strongswan capabilities
to NetworkManager.

%package sqlite
Summary: SQLite support for strongSwan
Requires: %{name} = %{version}-%{release}
%description sqlite
The sqlite plugin adds an SQLite database backend to strongSwan.

%package tnc-imcvs
Summary: Trusted network connect (TNC)'s IMC/IMV functionality
Requires: %{name} = %{version}-%{release}
Requires: %{name}-sqlite = %{version}-%{release}
%description tnc-imcvs
This package provides Trusted Network Connect's (TNC) architecture support.
It includes support for TNC client and server (IF-TNCCS), IMC and IMV message
exchange (IF-M), interface between IMC/IMV and TNC client/server (IF-IMC
and IF-IMV). It also includes PTS based IMC/IMV for TPM based remote
attestation, SWID IMC/IMV, and OS IMC/IMV. It's IMC/IMV dynamic libraries
modules can be used by any third party TNC Client/Server implementation
possessing a standard IF-IMC/IMV interface. In addition, it implements
PT-TLS to support TNC over TLS.

%prep
%setup -q -n %{name}-%{version}%{?prerelease}

%build
# only for snapshots
#autoreconf

# --with-ipsecdir moves internal commands to /usr/libexec/strongswan
# --bindir moves 'pki' command to /usr/libexec/strongswan
# See: http://wiki.strongswan.org/issues/552
# too broken to enable:    --enable-sha3 --enable-rdrand --enable-connmark --enable-forecast
%configure --disable-static \
    --with-ipsec-script=strongswan \
    --sysconfdir=%{_sysconfdir}/strongswan \
    --with-ipsecdir=%{_libexecdir}/strongswan \
    --bindir=%{_libexecdir}/strongswan \
    --with-ipseclibdir=%{_libdir}/strongswan \
    --with-fips-mode=2 \
    --enable-tss-trousers \
    --enable-nm \
    --enable-systemd \
    --enable-openssl \
    --enable-unity \
    --enable-ctr \
    --enable-ccm \
    --enable-gcm \
    --enable-chapoly \
    --enable-md4 \
    --enable-gcrypt \
    --enable-newhope \
    --enable-xauth-eap \
    --enable-xauth-pam \
    --enable-xauth-noauth \
    --enable-eap-identity \
    --enable-eap-md5 \
    --enable-eap-gtc \
    --enable-eap-tls \
    --enable-eap-ttls \
    --enable-eap-peap \
    --enable-eap-mschapv2 \
    --enable-eap-tnc \
    --enable-eap-sim \
    --enable-eap-sim-file \
    --enable-eap-aka \
    --enable-eap-aka-3gpp \
    --enable-eap-aka-3gpp2 \
    --enable-eap-dynamic \
    --enable-eap-radius \
    --enable-ext-auth \
    --enable-ipseckey \
    --enable-pkcs11 \
    --enable-tpm \
    --enable-farp \
    --enable-dhcp \
    --enable-ha \
    --enable-led \
    --enable-sql \
    --enable-sqlite \
    --enable-tnc-ifmap \
    --enable-tnc-pdp \
    --enable-tnc-imc \
    --enable-tnc-imv \
    --enable-tnccs-20 \
    --enable-tnccs-11 \
    --enable-tnccs-dynamic \
    --enable-imc-test \
    --enable-imv-test \
    --enable-imc-scanner \
    --enable-imv-scanner  \
    --enable-imc-attestation \
    --enable-imv-attestation \
    --enable-imv-os \
    --enable-imc-os \
    --enable-imc-swid \
    --enable-imv-swid \
    --enable-imc-swima \
    --enable-imv-swima \
    --enable-imc-hcd \
    --enable-imv-hcd \
    --enable-curl \
    --enable-cmd \
    --enable-acert \
    --enable-aikgen \
    --enable-vici \
    --enable-swanctl \
    --enable-duplicheck \
%ifarch x86_64 %{ix86}
    --enable-aesni \
%endif
    --enable-kernel-libipsec

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# mv %{buildroot}%{_sysconfdir}/strongswan/dbus-1 %{buildroot}%{_sysconfdir}/
# prefix man pages
for i in %{buildroot}%{_mandir}/*/*; do
    if echo "$i" | grep -vq '/strongswan[^\/]*$'; then
        mv "$i" "`echo "$i" | sed -re 's|/([^/]+)$|/strongswan_\1|'`"
    fi
done
find %{buildroot} -type f -name '*.la' -delete
# delete unwanted library files - no consumers, so no -devel package
rm %{buildroot}%{_libdir}/strongswan/*.so
# fix config permissions
chmod 644 %{buildroot}%{_sysconfdir}/strongswan/strongswan.conf

# Create ipsec.d directory tree.
install -d -m 700 %{buildroot}%{_sysconfdir}/strongswan/ipsec.d
for i in aacerts acerts certs cacerts crls ocspcerts private reqs; do
    install -d -m 700 %{buildroot}%{_sysconfdir}/strongswan/ipsec.d/${i}
done

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README NEWS TODO ChangeLog
%license COPYING
%dir %attr(0700,root,root) %{_sysconfdir}/strongswan
%config(noreplace) %{_sysconfdir}/strongswan/*
%dir %{_libdir}/strongswan
%exclude %{_libdir}/strongswan/imcvs
%dir %{_libdir}/strongswan/plugins
%dir %{_libexecdir}/strongswan
%{_unitdir}/strongswan.service
%{_unitdir}/strongswan-starter.service
%{_sbindir}/charon-cmd
%{_sbindir}/charon-systemd
%{_sbindir}/strongswan
%{_sbindir}/swanctl
%{_libdir}/strongswan/*.so.*
%exclude %{_libdir}/strongswan/libimcv.so.*
%exclude %{_libdir}/strongswan/libtnccs.so.*
%exclude %{_libdir}/strongswan/libipsec.so.*
%{_libdir}/strongswan/plugins/*.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-sqlite.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so
%{_libexecdir}/strongswan/*
%exclude %{_libexecdir}/strongswan/attest
%exclude %{_libexecdir}/strongswan/pt-tls-client
%exclude %{_libexecdir}/strongswan/charon-nm
%exclude %dir %{_datadir}/strongswan/swidtag
%{_mandir}/man?/*.gz
%{_datadir}/strongswan/templates/config/
%{_datadir}/strongswan/templates/database/

%files sqlite
%{_libdir}/strongswan/plugins/libstrongswan-sqlite.so

%files tnc-imcvs
%{_sbindir}/sw-collector
%{_sbindir}/sec-updater
%dir %{_libdir}/strongswan/imcvs
%dir %{_libdir}/strongswan/plugins
%{_libdir}/strongswan/libimcv.so.*
%{_libdir}/strongswan/libtnccs.so.*
%{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%{_libexecdir}/strongswan/attest
%{_libexecdir}/strongswan/pt-tls-client
%dir %{_datadir}/strongswan/swidtag
%{_datadir}/strongswan/swidtag/*.swidtag

%files libipsec
%{_libdir}/strongswan/libipsec.so.*
%{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so

%files charon-nm
%doc COPYING
#%{_sysconfdir}/dbus-1/system.d/nm-strongswan-service.conf
%{_datadir}/dbus-1/system.d/nm-strongswan-service.conf
%{_libexecdir}/strongswan/charon-nm
