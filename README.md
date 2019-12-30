# GridScale Task - MicroServices architecture based application

## How to install locally:
### 1- install Kubernetes
```text
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && sudo install kubectl /usr/local/bin && rm kubectl
```

### 2- install minikube:
2-1- First install KVM driver

```text
curl -LO https://storage.googleapis.com/minikube/releases/latest/docker-machine-driver-kvm2 \
    && sudo install docker-machine-driver-kvm2 /usr/local/bin/ && rm docker-machine-driver-kvm2
```
2-2- Then install Minikube
```text
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
    && sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
2-3- verify installation:
```text
minikube version
```
2-4- set KVM as default driver:
```text
minikube config set vm-driver kvm2
```
2-5- start minikube:
```text
minikube start
```

### 3- Install Helm:
```
$ curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
$ chmod 700 get_helm.sh
$ ./get_helm.sh
$  helm repo add stable https://kubernetes-charts.storage.googleapis.com
$ helm repo update

```
### 3- enable ingress
```shell
minikube addons enable ingress
```

### 4- install nginx ingress controller:
```text
helm install nginx-ingress stable/nginx-ingress --set controller.publishService.enabled=true
```

### 5- Add minikube ip to your local DNS:
```text
echo "$(minikube ip) local.gridscale.com" | sudo tee -a /etc/hosts
```
:
### 6- Install Skaffold
```text
https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64  -O /usr/local/bin/skaffold
chmod +x  /usr/local/bin/skaffold
```

### 7- Run Skaffold:
```text
skaffold dev --namespace=gridscale --default-repo localhost:3200
```
When all pods are deployed and all the tasks are completely run you can see some output like this:
```text
[product-5dc6547d48-wc5vx product-web] 115 static files copied to '/code/files/static'.
[product-migrations-jjjvl product-migration] No changes detected
[product-5dc6547d48-wc5vx product-web] Performing system checks...
[product-5dc6547d48-wc5vx product-web] 
[product-5dc6547d48-wc5vx product-web] System check identified no issues (0 silenced).
[product-5dc6547d48-wc5vx product-web] December 30, 2019 - 17:59:30
[product-5dc6547d48-wc5vx product-web] Django version 1.11.26, using settings 'conf.settings'
[product-5dc6547d48-wc5vx product-web] Starting development server at http://0.0.0.0:8000/
[product-5dc6547d48-wc5vx product-web] Quit the server with CONTROL-C.
[product-migrations-jjjvl product-migration] Operations to perform:
[product-migrations-jjjvl product-migration]   Apply all migrations: admin, auth, contenttypes, product, sessions
[product-migrations-jjjvl product-migration] Running migrations:
[product-migrations-jjjvl product-migration]   No migrations to apply.
[product-migrations-jjjvl product-migration] Installed 10000 object(s) from 1 fixture(s)
```
### 8- Run import_runner script:
After all pods are deployed, you can easily import the provided CSV database using **csv_import.py** script inside **import_runner** directory:
```css
cd import_runner
pip3 install requirements.txt
python3.5 csv_import.py --csv orders.csv
```
## Endpoints:
1. Customer Endpoint: 
- Base: http://local.gridscale.com/customer/api/1.0/customer/
- Docs: http://local.gridscale.com/customer/api/1.0/docs/

2. Product Endpoint: 
- Base: http://local.gridscale.com/product/api/1.0/product/
- Docs: http://local.gridscale.com/product/api/1.0/docs/

3. Order Endpoint: 
- Base: http://local.gridscale.com/order/api/1.0/order/
- Docs: http://local.gridscale.com/order/api/1.0/docs/

## Notes:
1. `Schema-per-service` pattern is used for each microservice - each service has a database schema that’s private to that service.
2. `API Composition` is used to implement queries in a microservice architecture

