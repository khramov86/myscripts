%define debug_package %{nil}
%define _name   etcd
%define _user	etcd
%define _group	etcd
%define _etcdata /data/etcd
%define _conf_dir    %{_sysconfdir}/%{_name}
%define _localbindir /usr/local/bin
#%undefine _disable_source_fetch

Name:		etcd
Version:	%{version}
Release:	%{build_number}
Summary:	A distributed, reliable key-value store for the most critical data of a distributed system
License:	Apache License, Version 2.0
URL:		https://github.com/etcd-io/etcd			
Conflicts:	etcd

Source0:	https://github.com/etcd-io/etcd/releases/download/v%{version}/etcd-v%{version}-linux-amd64.tar.gz
Source1:	%{_name}.service	
Source2:	%{_name}.conf

%{?systemd_requires}
Requires(pre): shadow-utils

%description

A distributed, reliable key-value store for the most critical data of a distributed system

%prep
%setup -q -n %{name}-v%{version}-linux-amd64


%build
/bin/true

%install

cat << EOF >  $RPM_SOURCE_DIR/%{_name}.service 
[Unit]
Description=etcd key-value store
Documentation=https://github.com/etcd-io/etcd 
After=network.target

[Service]
User=etcd
Type=notify
ExecStart=/usr/local/bin/etcd --config-file /etc/etcd.conf
Restart=always
RestartSec=10s
LimitNOFILE=40000

[Install]
WantedBy=multi-user.target

EOF

cat << EOF >  $RPM_SOURCE_DIR/%{_name}.conf
name: default 
data-dir: /data/etcd
initial-advertise-peer-urls: http://$(hostname):2380
listen-peer-urls: http://0.0.0.0:2380
listen-client-urls: http://0.0.0.0:2379
advertise-client-urls: http://$(hostname):2379
initial-cluster: default=http://$(hostname):2380
enable-v2: true

EOF

mkdir -vp %{buildroot}%{_etcdata}
mkdir -vp %{buildroot}%{_localbindir}

for etcdbin in  etcd etcdctl; do
  install -D -m 755 ${etcdbin} %{buildroot}%{_localbindir}/${etcdbin}
done

install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{_name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r -g %{_group} -s /bin/bash -c "etcd services" %{_user}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_localbindir}/etcd
%{_localbindir}/etcdctl
%config(noreplace) %{_sysconfdir}/%{_name}.conf 
%{_unitdir}/%{_name}.service
%dir %attr(755, %{_user}, %{_group})%{_etcdata}
