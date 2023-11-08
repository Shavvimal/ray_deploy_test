kind create cluster --image=kindest/node:v1.23.0
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0-rc.0
kubectl apply -f config/custom.yaml
kubectl describe pods -l=ray.io/is-ray-node=yes
kubectl get pods -l=ray.io/is-ray-node=yes
# Delete service
kubectl delete rayservice rayservice-dummy