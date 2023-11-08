# Context kubectl
aws eks update-kubeconfig --region eu-west-2 --name ray-test
# KubeRay Operator
helm install kuberay-operator kuberay/kuberay-operator --version 1.0.0-rc.0
# AWS Load Balancer Controller
eksctl utils associate-iam-oidc-provider \
    --region eu-west-2 \
    --cluster ray-test \
    --approve
eksctl create iamserviceaccount \
    --cluster=ray-test \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::12345678910:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --region eu-west-2 \
    --approve
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=ray-test --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
# Ray Custom Resource Definition
kubectl apply -f config/custom.yaml
kubectl get pods -l=ray.io/is-ray-node=yes
kubectl describe pods -l=ray.io/is-ray-node=yes
kubectl describe rayservice rayservice-dummy
# Ingress
kubectl apply -f config/ingress.yaml
kubectl describe ingress # ADD NAME
# Grafana
kubectl cp rayservice-dummy-raycluster-gqxb2-head-cgpkf:/tmp/ray/session_latest/metrics/grafana/dashboards/ ./config/grafana/
# Dashboard Forwarding Local
kubectl port-forward svc/rayservice-dummy-head-svc --address 0.0.0.0 8265:8265
# Get EKS Config
./eksctl get cluster ray-test
# Delete service
kubectl delete rayservice rayservice-dummy
kubectl get ingress
kubectl delete ingress ray-cluster-ingress