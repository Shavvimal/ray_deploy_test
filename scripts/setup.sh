kind create cluster --image=kindest/node:v1.23.0
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0-rc.0
curl -o demo.yaml  https://raw.githubusercontent.com/ray-project/kuberay/v1.0.0-rc.0/ray-operator/config/samples/ray_v1alpha1_rayservice.yaml
kubectl apply -f demo.yaml
kubectl get pods -l=ray.io/is-ray-node=yes