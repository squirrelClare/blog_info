# elasticsearch和kibana部署
---
## 版本信息：
- elasticsearch: 7.17.5
- kibana: 7.17.5
## 前置条件
- k8s已部署且webui为rancher；
- k8s支持由storageClass来创建pv并绑定pvc
## elasticsearch部署
### master
依次根据master文件夹内的：es-master-config.yml、es-master-deploment.yml、 es-master-service.yml部署master服务。
### dataNode
依次根据data文件夹内的：es-data-config.yml、es-data-stateful.yml、 es-data-service.yml部署data服务。
### client
依次根据client文件夹内的：es-client-config.yml、es-client-dep.yml、 es-client-service.yml部署client服务。
### ca秘钥
进入master容器依次执行：
- `./bin/elasticsearch-certutil ca`
- `./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12 `

进入宿主机将秘钥elastic-certificates.p12复制到本地，然后依次分发到master、data、client几点对应pv的certs目录下

- 容器复制到本地:
```
kubectl cp ems/elasticsearch-master-7b7d67b6f6-2vdhk:/usr/share/elasticsearch/data/certs/elastic-certificates.p12 ./elastic-certificates.p12
```
- 本地到容器: 
```
kubectl cp ./elastic-certificates.p12 ems/elasticsearch-data-1:/usr/share/elasticsearch/data/certs/elastic-certificates.p1
```
### 初始化密码
进入client节点，执行下属命令生成密码：
```
bin/elasticsearch-setup-passwords auto -b
```
如：
```
Changed password for user apm_system
PASSWORD apm_system = 5wg8JbmKOKiLMNty90l1

Changed password for user kibana_system
PASSWORD kibana_system = 1bT0U5RbPX1e9zGNlWFL

Changed password for user kibana
PASSWORD kibana = 1bT0U5RbPX1e9zGNlWFL

Changed password for user logstash_system
PASSWORD logstash_system = 1ihEyA5yAPahNf9GuRJ9

Changed password for user beats_system
PASSWORD beats_system = WEWDpPndnGvgKY7ad0T9

Changed password for user remote_monitoring_user
PASSWORD remote_monitoring_user = MOCszTmzLmEXQrPIOW4T

Changed password for user elastic
PASSWORD elastic = bbkrgVrsE3UAfs2708aO
```
抽取elastic的密码和用户名在rancher中生成密文资源：elastic-credentials
## kibana部署
依次执行kibana目录内的kibana.configmap.yml、kibana.deployment.yml、kibana.ingress.yml、kibana.service.yml。