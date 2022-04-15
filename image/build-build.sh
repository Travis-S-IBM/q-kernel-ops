#!/usr/bin/bash

VERSION=0.0.0

#ANARCH=aarch64
#TAGARCH=a

#ANARCH=x86_64
#TAGARCH=x

#ANARCH=ppc64le
#TAGARCH=p

ANARCH=s390x
TAGARCH=z

ANOS=Linux
ANYEAR=2021
ANVERS=11

TAG=${VERSION}-${TAGARCH}

ANACONDA_INSTALLER=Anaconda3-${ANYEAR}.${ANVERS}-${ANOS}-${ANARCH}.sh

cp ../requirements*.txt . 
sed -i 's/pyarrow//g' requirements.txt

podman build .  -t quay.io/qiskit/qmlbuild:${TAG} --build-arg=ANCONDA_INSTALLER=${ANACONDA_INSTALLER} --file=Dockerbuild

podman push quay.io/qiskit/qmlbuild:${TAG}

