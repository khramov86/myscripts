%define debug_package %{nil}
%define _name	postgres_exporter	
%define _user	promethues
%define _group	prometheus
%define _conf_dir    %{_sysconfdir}/%{_name}
%define _localbindir /usr/local/bin
#%undefine _disable_source_fetch

Name:		postgres-exporter
Version:	%{version}
Release:	%{build_number}
Summary:	Prometheus exporter for PostgreSQL server metrics.
License:	Apache License, Version 2.0
URL:		https://github.com/wrouesnel/postgres_exporter
Conflicts:	prometheus-exporter

Source0:	https://github.com/wrouesnel/postgres_exporter/releases/download/v%{version}/postgres_exporter_v%{version}_linux-amd64.tar.gz
Source1:	%{name}.service
Source2:	%{name}
#Source3:	queries.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for PostgreSQL server metrics.
CI Tested PostgreSQL versions: 9.4, 9.5, 9.6, 10, 11

%prep
%setup -q -n %{_name}_v%{version}_linux-amd64 

%build
/bin/true

%install
cat <<EOF > $RPM_SOURCE_DIR/%{name}
DATA_SOURCE_NAME="postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
EOF

cat <<EOF > $RPM_SOURCE_DIR/%{name}.service
[Unit]
Description=PostgreSQL Exporter
Documentation=https://github.com/wrouesnel/postgres_exporter
After=network.target

[Service]
User=%{_user}
Group=%{_group}
Restart=on-failure
EnvironmentFile=/etc/sysconfig/%{name}
ExecStart=%{_localbindir}/%{_name}
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=postgres-exporter

[Install]
WantedBy=multi-user.target
EOF

mkdir -vp %{buildroot}%{_localbindir}
install -D -m 644 %{_name} %{buildroot}%{_localbindir}/%{_name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r -g %{_group} -s /bin/bash -c "prometheus services" %{_user}

%post
%systemd_post %{name}.service
ln -sf %{_localbindir}/%{_name} %{_bindir}/

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service
rm -f %{_localbindir}/%{_name}

%files
%defattr(-,root,root,-)
%{_localbindir}/%{_name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755, %{_user}, %{_group})%{_localbindir}/%{_name}
