#! /bin/bash

git diff --quiet HEAD
if [ "$?" -ne "0" ]; then
	echo git tree dirty, exiting
	exit 1
fi

tag=`git describe --tag --exact-match`
if [ "$?" -ne "0" ]; then
	echo no git tag exists, exiting
	exit 1
fi

this_script=$(realpath "$0")
wdir=$(dirname "$this_script")


cd $wdir/../../
make dist



cd $wdir
rm -rf ./build_data/
mkdir ./build_data/

if [ `ls ../../dist/*.whl | wc -l` -ne "1" ]; then
	echo Wrong number of whl files in dist dir, `pwd`, $wdir
	exit 1

fi
cp ../../dist/*.whl ./build_data/


docker build --tag $(minikube ip):5000/cc-service-search:${tag} .
docker build --tag $(minikube ip):5000/cc-service-search:latest .
docker push $(minikube ip):5000/cc-service-search:${tag}
docker push $(minikube ip):5000/cc-service-search:latest


