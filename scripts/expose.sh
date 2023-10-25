kubectl port-forward service/rayservice-dummy-head-svc 8000
kubectl port-forward svc/rayservice-dummy-head-svc --address 0.0.0.0 8265:8265