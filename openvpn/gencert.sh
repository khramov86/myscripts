#!/usr/bin/env bash
echo "Starting script"
OPENVPN_SERVER_HOST=IP_OR_HOSTNAME
USERNAME=$1
EASY_RSA_DIR=./easy-rsa
PUBLIC_CERTS_DIR=${EASY_RSA_DIR}/pki/issued
PRIVATE_CERTS_DIR=${EASY_RSA_DIR}/pki/private
TLS_KEY_PATH=./server/tc.key
if [ -z $USERNAME ]
  then echo -e "First parameter shouldn't be empty\n"
    while [ -z $USERNAME ]
      do
        read -p "Please, enter username: " USERNAME
      done
fi
echo "Generating config for username $USERNAME"
check_if_user_exists()
{
if [ -f $PUBLIC_CERTS_DIR/$USERNAME.crt ]
  then echo -e "Certificate for $USERNAME exists\ncontinue"
else
  echo "There is no such username, please recreate certificate"
  AVAILABLE_CERTS=$(ls ./easy-rsa/pki/issued/ |grep -v server |awk -F\. '{print $1}')
  echo "Please chose one of these users"
    for USER in $AVAILABLE_CERTS
      do echo "* $USER"
    done 
  exit 1
fi
}
gen_config()
{
TLS_KEY=$(echo "<tls-auth>
$(cat ${TLS_KEY_PATH})
</tls-auth>")
USER_CERT=$(echo "<cert>
$(cat ${PUBLIC_CERTS_DIR}/${USERNAME}.crt)
</cert>")
USER_KEY=$(echo "<key>
$(cat ${PRIVATE_CERTS_DIR}/${USERNAME}.key)
</key>")
CA_CERT=$(echo "<ca>
$(cat ./easy-rsa/pki/ca.crt)
</ca>")
echo "Creating OVPN config $USERNAME.ovpn"
echo "client
resolv-retry infinite
nobind
remote $OPENVPN_SERVER_HOST
proto tcp
dev tun
;comp-lzo
cipher AES-256-CBC
;tls-client
key-direction 1
float
persist-key
persist-tun
verb 3
;remote-cert-tls server
reneg-sec 0
${CA_CERT}
${USER_CERT}
${USER_KEY}
${CA_CERT}
" > $USERNAME.ovpn
echo "Done"
}

check_if_user_exists
gen_config
