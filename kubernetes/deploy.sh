#! /bin/bash

helm dep update helm
helm dependency build helm
helm install cc-service-search helm --create-namespace -n cc-service-search
