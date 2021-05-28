
Name:           node_exporter
Version:        0.18.1
Release:        0
Summary:        Exporter for machine metrics
License:        ASL 2.0
URL:            https://github.com/prometheus/node_exporter
#BuildRoot:     ~/rpmbuild/
Source:         /usr/local/bin/node_exporter-0.18.1.linux-amd64.tar.gz
#Source0:        /usr/local/bin/node_exporter/node_exporter
#Source1:        /usr/local/bin/node_exporter/LICENSE
#Source2:        /usr/local/bin/node_exporter/NOTICE
#Source3:        /etc/systemd/system/node_exporter.service
%description
%prep
%files
#%attr(0744, node_exporter, node_exporter) /usr/local/bin/node_exporter/*
#%attr(0644, root, root) /etc/systemd/system/node_exporter.service
%node_exporter-0.18.1.linux-amd64.tar.gz
%build
%install
%pre
useradd -rs /bin/false node_exporter -c "Prometheus node exporter" node_exporter
%post
tar -xvf /usr/local/bin/node_exporter-0.18.1.linux-amd64.tar.gz 
mv /usr/local/bin/node_exporter-0.18.1.linux-amd64 /usr/local/bin/node_exporter
chown -R node_exporter /usr/local/bin/node_exporter/*
echo "[Unit]\n Description=Node Exporter\n After=network.target\n [Service]\n User=node_exporter\n Group=node_exporter\n Type=simple\n ExecStart=/usr/local/bin/node_exporter\n [Install]\n WantedBy=multi-user.target\n" > /etc/systemd/system/node_exporter.service
chmod 640 /etc/systemd/system/node_exporter.service
chown root:root /etc/systemd/system/node_exporter.service
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter
firewall-cmd --add-port=9100/tcp --zone=public --permanent
firewall-cmd --reload
