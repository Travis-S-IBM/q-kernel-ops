#!/usr/bin/bash

VERSION=0.0.4

#ANARCH=aarch64
#TAGARCH=a

#ANARCH=x86_64
#TAGARCH=x

#ANARCH=ppc64le
#TAGARCH=p

export ANARCH=s390x
export TAGARCH=z

export ANOS=Linux
export ANYEAR=2021
export ANVERS=11

export TAG=${VERSION}-${TAGARCH}

ANACONDA_INSTALLER=Anaconda3-${ANYEAR}.${ANVERS}-${ANOS}-${ANARCH}.sh


cp ../requirements.txt . 
cp ../studies/requirements.txt ./requirements-dev.txt
sed -i '/pyarrow/d' requirements.txt
sed -i '/pyarrow/d' requirements-dev.txt

podman build .  -t quay.io/qiskit/qmlbuild:${TAG} --build-arg=ANCONDA_INSTALLER=${ANACONDA_INSTALLER} --file=Dockerbuild
podman push quay.io/qiskit/qmlbuild:${TAG}

cp -r ../src .
cp ../workflow.py .

podman build .  -t quay.io/qiskit/qmlrun:${TAG} --file=Dockerfile
podman push quay.io/qiskit/qmlrun:${TAG} 
