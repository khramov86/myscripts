# Workarounds/Solutions

## Проблемы при обновлении

### Не качается образ или необходимо обновить пулл-сикрет

Получить новый 
https://console.redhat.com/openshift/install/metal/user-provisioned

Пропатчить
`oc set data secret/pull-secret -n openshift-config --from-file=/path/to/json_file`

### ImagePrunerDegraded при обновлении 4.5 -> 4.6

```
oc patch imagepruner.imageregistry/cluster --patch '{"spec":{"suspend":true}}' --type=merge
oc -n openshift-image-registry delete jobs --all
```
Проверки
```
oc describe co image-registry
oc get clusterversion -w -o wide
```

### Обновление сертификата для ингресс
```
oc create secret tls router-certs4 --cert=/path_to_fullchain.pem --key=/path_to_pk.pem -n openshift-ingress
oc patch ingresscontroller default -n openshift-ingress-operator --type=merge --patch='{"spec": { "defaultCertificate": { "name": "router-certs4" }}}'
```

### Фриз обновления 
Проверить на нодах
```
podman images
```
Если там есть сообщения типа layer not known - вычистить слои для имиджей
```
rm -rf /var/lib/containers/storage/overlay-images
```
Посмотреть, что поды создаются:
```
watch "crictl ps -a"
```
### У части подов ошибка imagepullbackoff 
Просмотреть поды с проблемами pull image
```
oc get po -A |grep Image
```
Попробоват пересоздать
```
oc get po -A |grep Image |awk '{print "oc -n",$1,"delete po",$2}'
```
### Проблемы с repo

Проверить, какие repo включены в FCOS
```
fgrep enabled /etc/yum.repos.d/* | uniq -c
```
Попробовать задеплоить machineconfig
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-provisioning-workaround
  labels:
    machineconfiguration.openshift.io/role: worker
spec:
  config:
    ignition:
      version: 3.2.0
    storage:
      files:
        - contents:
            source: >-
              data:text/plain,%23%21%2Fbin%2Fbash%0Aset%20-euo%20pipefail%0AIFS%3D%24%27%5Cn%5Ct%27%0A%0ATO_PROCESS_IGNITION_FILE%3D%22%2Fetc%2Fignition-machine-config-encapsulated.json%22%0APROCESSED_IGNITION_FILE%3D%22%24%7BTO_PROCESS_IGNITION_FILE%7D.bak%22%0AIGNITION_FILE_ORIGINAL_BACKUP%3D%22%24%7BTO_PROCESS_IGNITION_FILE%7D.original%22%0AIGNITION_FILE_NOEXTENSION_FINAL%3D%22%24%7BTO_PROCESS_IGNITION_FILE%7D.no_extensions_workaround%22%0A%0Aif%20%5B%20-e%20%22%24%7BIGNITION_FILE_NOEXTENSION_FINAL%7D%22%20%5D%3B%20then%0A%20%20%23echo%20%22We%20shouldn%27t%20get%20here%2C%20nothing%20to%20do.%22%0A%20%20exit%200%0Aelif%20%5B%20%21%20-e%20%22%24%7BIGNITION_FILE_ORIGINAL_BACKUP%7D%22%20%5D%3B%20then%0A%20%20%23First%20run%20machine-config-daemon%20firstboot-complete-machineconfig%20with%20modified%20ignition%20file%0A%20%20mv%20%22%24%7BTO_PROCESS_IGNITION_FILE%7D%22%20%22%24%7BIGNITION_FILE_ORIGINAL_BACKUP%7D%22%0A%20%20jq%20-cM%20%27del%20%28.spec.extensions%5B%5D%29%27%20%22%24%7BIGNITION_FILE_ORIGINAL_BACKUP%7D%22%20%3E%20%22%24%7BTO_PROCESS_IGNITION_FILE%7D%22%0A%20%20%2Frun%2Fbin%2Fmachine-config-daemon%20firstboot-complete-machineconfig%0A%20%20%23The%20machine%20will%20reboot%0Aelse%0A%20%20%23Second%20run%20machine-config-daemon%20firstboot-complete-machineconfig%20with%20original%20ignition%20file%0A%20%20mv%20%22%24%7BPROCESSED_IGNITION_FILE%7D%22%20%22%24%7BIGNITION_FILE_NOEXTENSION_FINAL%7D%22%0A%20%20mv%20%22%24%7BIGNITION_FILE_ORIGINAL_BACKUP%7D%22%20%22%24%7BTO_PROCESS_IGNITION_FILE%7D%22%0A%20%20%2Frun%2Fbin%2Fmachine-config-daemon%20firstboot-complete-machineconfig%0A%20%20%23The%20machine%20will%20reboot%0Afi%0A%0Aecho%20%22Waiting%20for%20machine%20to%20reboot...%22%0Asleep%2030%0Aecho%20%22It%20doesn%27t%20look%20like%20the%20machine%20ever%20rebooted%21%22
          mode: 755
          overwrite: true
          path: /usr/local/sbin/provisioning-workaround.sh
    systemd:
      units:
        - contents: |
            [Unit]
            Description=Alternate Machine Config Daemon Firstboot
            # Make sure it runs only on OSTree booted system
            ConditionPathExists=/run/ostree-booted
            # Removal of this file signals firstboot completion
            ConditionPathExists=|/etc/ignition-machine-config-encapsulated.json
            ConditionPathExists=|/etc/ignition-machine-config-encapsulated.json.original
            After=machine-config-daemon-pull.service
            Before=crio.service crio-wipe.service
            Before=kubelet.service

            [Service]
            Type=oneshot
            RemainAfterExit=yes
            # Disable existing repos (if any) so that OS extensions would use embedded RPMs only
            ExecStartPre=-/usr/bin/sh -c "sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/*.repo"
            ExecStart=/usr/local/sbin/provisioning-workaround.sh
            [Install]
            WantedBy=multi-user.target
            RequiredBy=crio.service kubelet.service
          enabled: true
          name: machine-config-daemon-firstboot.service
  extensions: null
  fips: false
  kernelArguments: null
  kernelType: ''
  osImageURL: ''
  ```
Очистить все пакеты
```
sudo rpm-ostree uninstall --all
```
