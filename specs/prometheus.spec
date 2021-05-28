%define debug_package %{nil}
%define _name	prometheus
%define _user	prometheus
%define _group	prometheus
%define _conf_dir    %{_sysconfdir}/%{_name}
%define _localbindir /usr/local/bin
#%undefine _disable_source_fetch

Name:		prometheus
Version:	%{version}
Release:	%{build_number}
Summary:	Prometheus is a free software application used for event monitoring and alerting.	
License:	Apache License, Version 2.0
URL:		https://github.com/prometheus/prometheus
Conflicts:	prometheus

Source0:	https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1:	%{_name}.service	
Source2:	%{_name}

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus is a free software application used for event monitoring and alerting.

%prep
%setup -q -n %{name}-%{version}.linux-amd64


%build
/bin/true

%install
cat <<EOF > $RPM_SOURCE_DIR/%{_name}
OPTIONS="--config.file=/etc/prometheus/prometheus.yml \
--storage.tsdb.path=/var/lib/prometheus/"
EOF

cat <<EOF > $RPM_SOURCE_DIR/%{_name}.service
[Unit]
Description=Prometheus Server
Documentation=https://github.com/prometheus/prometheus
[Service]
Restart=always
User=prometheus
Group=prometheus
EnvironmentFile=/etc/sysconfig/prometheus
ExecStart=/usr/local/bin/prometheus \$OPTIONS
ExecReload=/bin/kill -HUP \$MAINPID
TimeoutStopSec=20s
SendSIGKILL=no
[Install]
WantedBy=multi-user.target
EOF

mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
mkdir -vp %{buildroot}%{_localbindir}
#mkdir -vp %{buildroot}%{_bindir}

for prombin in prometheus promtool; do
  install -D -m 755 ${prombin} %{buildroot}%{_localbindir}/${prombin}
done

for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -D -m 644 ${file} %{buildroot}%{_datarootdir}/prometheus/${file}
  done
done
install -D -m 644 prometheus.yml %{buildroot}%{_sysconfdir}/prometheus/prometheus.yml
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/prometheus.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/prometheus

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r -g %{_group} -s /bin/bash -c "prometheus services" %{_user}

%post
%systemd_post %{name}.service
ln -sf %{_localbindir}/promtool %{_bindir}/
ln -sf %{_localbindir}/prometheus %{_bindir}/

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service
rm -f %{_bindir}/prometheus
rm -f %{_bindir}/promtool

%files
%defattr(-,root,root,-)
%{_localbindir}/prometheus
%{_localbindir}/promtool
%config(noreplace) %{_sysconfdir}/prometheus/prometheus.yml
%{_datarootdir}/prometheus
%{_unitdir}/prometheus.service
%config(noreplace) %{_sysconfdir}/sysconfig/prometheus
%dir %attr(755, %{_user}, %{_group})%{_sharedstatedir}/prometheus
