#/usr/bin/env bash
declare -A INVENTORY
ID_GROUP=200
#let IDGROUP++
function counter()
{
        let ID_GROUP++
        echo $ID_GROUP
}
INVENTORY=( \
        [mas1]="DE:89:EB:84:82:25,$(( ID_GROUP + 1 ))" \
        [mas2]="26:B0:96:2E:68:FF,$(( ID_GROUP + 2 ))" \
        [mas3]="28:A5:67:4B:36:DF,$(( ID_GROUP + 3 ))" \
        [work1]="D2:E2:45:90:28:A1,$(( ID_GROUP + 4 ))" \
        [work2]="02:D8:49:1B:46:EE,$(( ID_GROUP + 5 ))" \
        [boot]="36:25:A6:89:2E:B1,$(( ID_GROUP + 9 ))" \
        )
VLANID=2000
for host in ${!INVENTORY[@]}
  do
    hostid=`echo ${INVENTORY[$host]} |awk -F\, '{print $2}'`
    hostmac=`echo ${INVENTORY[$host]} |awk -F\, '{print $1}'`
    hostlist="$(qm list |awk '{print $1}')"
      if [[ "$hostlist" =~ "$hostid" ]]; then
        echo "VM exists, skipping"
      else
        echo "Creating VM"
        qm clone 5002 $hostid --full=yes --name="oc-$host"
      fi
    echo "Setting VLANs for VM $host with $hostid"
    qm set $hostid --net0 virtio,firewall=0,macaddr=${hostmac},tag=${VLANID}
    echo "Starting VM"
    qm start $hostid
done
