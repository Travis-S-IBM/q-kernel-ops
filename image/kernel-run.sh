#!/usr/bin/bash
#
# usage: 
#
# 0. Log in to your IBM Quantum Services account
#    go to your account profile & copy your auth token 
#
# 1. configure default-env file as described in README.md
#
# 2. now run this script
#


podman run -d -v ${HOME}/${REPO}/${DATA}:/${DATA} \
       -e QS_TOKEN=${QS_TOKEN}                    \
       -e BACKEND="ibmq_qasm_simulator"           \
       -e MATRIX_SIZE=${MATRIX_SIZE}              \
       -e CIRCUIT_ID=${CIRGUIT_ID}                \
       -e LAYER=${LAYER}                          \
       quay.io/qiskit/qmlrun:0.0.4-z 


