# 清华大学微博

Final project for the Distributed Database Systems course at Tsinghua University (2022).

# Usage

Requires a working `minikube` installation. To start the application, run the following commands.

```
minikube start
kubectl apply -f kube
```

# Services

Access Grafana (Metrics and Monitoring) at http://localhost:3000.
```
kubectl port-forward services/grafana 3000:3000
```

Access Prometheus (Metrics and Monitoring) at http://localhost:9090.
```
kubectl port-forward services/grafana 9090:9090
```
