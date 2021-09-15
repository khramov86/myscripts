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
