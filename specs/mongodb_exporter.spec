%define debug_package %{nil}
%define _user   prometheus
%define _group  prometheus
%define _conf_dir    %{_sysconfdir}/%{name}
%define _localbindir /usr/local/bin
#%undefine _disable_source_fetch


Name:           mongodb_exporter
Version:        0.20.1
Release:        1%{?dist}
Summary:        Based on MongoDB exporter by David Cuadrado (@dcu), but forked for full sharded support and structure changes.

License:        Apache License 2.0
URL:            https://github.com/percona/mongodb_exporter
Conflicts:      %{name}
Source0:        https://github.com/percona/mongodb_exporter/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1:        %{name}.service
Source2:        %{name}

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Based on MongoDB exporter by David Cuadrado (@dcu), but forked for full sharded support and structure changes.

%prep
%setup -q -c

%build
/bin/true

%install
cat <<EOF > $RPM_SOURCE_DIR/%{name}
MONGODB_URI=mongodb://mongodb_exporter:password@localhost:27017
EOF

cat <<EOF > $RPM_SOURCE_DIR/%{name}.service
[Unit]
Description=MongoDB Exporter
Documentation=https://github.com/percona/mongodb_exporter
After=network.target

[Service]
User=%{_user}
Group=%{_group}
Restart=on-failure
EnvironmentFile=/etc/sysconfig/%{name}
ExecStart=/usr/local/bin/%{name}
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%{name}

[Install]
WantedBy=multi-user.target
EOF

mkdir -vp %{buildroot}%{_localbindir}
install -D -m 644 %{name} %{buildroot}%{_localbindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r -g %{_group} -s /bin/bash -c "prometheus services" %{_user}

%post
%systemd_post %{name}.service
ln -sf %{_localbindir}/%{name} %{_bindir}/

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service
rm -f %{_localbindir}/%{name}

%files
%defattr(-,root,root,-)
%{_localbindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(755, %{_user}, %{_group})%{_localbindir}/%{name}