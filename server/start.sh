#! /bin/bash

helm repo add opensearch-project-helm-charts https://opensearch-project.github.io/helm-charts

ns=cc-service-search
kubectl create ns $ns
helm install  -n $ns  \
	--set sysctlInit.enabled=True \
	--set replicas=1 \
	--set service.nodePort=32123 \
	--set service.type=NodePort \
	cc-opensearch opensearch-project-helm-charts/opensearch


minikube service opensearch-cluster-master -n $ns --url
echo Minikube connection addr: `minikube ip`:32123
