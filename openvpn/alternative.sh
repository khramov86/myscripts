#!/usr/bin/env bash

tempalate="client
remote maximo.shell-azs.ru
comp-lzo
port 1194
proto tcp
dev tun
dev-type tun
resolv-retry infinite
nobind
persist-key
persist-tun
verb 3
tls-client
key-direction 1
remote-cert-tls server
"

BASE_DIR=/etc/openvpn/easyrsa
CA_SERT=pki/ca.crt
TA_PATH=pki/ta.key
cd $BASE_DIR
if [[ -z "$1" ]]; then
        echo "One argument should be passed"
        exit 1
else
        echo "Generating config for $1"
fi

CERT=pki/issued/$1.crt
KEY=pki/private/$1.key

if [[ ! -f $CERT || ! -f $KEY ]]; then
        echo "No such file, possbile certs are:"
        for i in $(ls pki/issued/); do echo -en "  "; basename $i .crt;done
        exit 1
fi

echo "$tempalate" > $1.ovpn
echo "<ca>
$(cat $CA_SERT)
</ca>
<cert>
$(cat $CERT)
</cert>
<key>
$(cat $KEY)
</key>
<tls-auth>
$(cat $TA_PATH)
</tls-auth>
" >> ./$1.ovpn
