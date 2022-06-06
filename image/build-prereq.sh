#!/usr/bin/bash

VERSION=0.0.3

#TAGARCH=a

#TAGARCH=x

#TAGARCH=p

TAGARCH=z

export TAG=${VERSION}-${TAGARCH}

cp -r ../src .
cp ../workflow.py .
cp -r ../studies .

podman build .  -t quay.io/qiskit/qmlpre:${TAG} --file=Dockerprereq
podman push quay.io/qiskit/qmlpre:${TAG} 
