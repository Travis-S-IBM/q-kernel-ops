#!/usr/bin/bash
#
# usage: 
#
# 0. Log in to your IBM Quantum Services account
#    go to your account profile & copy your auth token 
#
# 1. put your Quantum Services token in an enviroment
#    variable called QS_TOKEN:
#
#  $ export QS_TOKEN="your-big-old-Quantum-services-token"
#
# 2. now run this script
#

export REPO=q-kernel-ops
export DATA=resources/kernel_metadata

podman run -d -v ${HOME}/${REPO}/${DATA}:/${DATA} \
       -e QS_TOKEN=${QS_TOKEN}                    \
       -e BACKEND="ibmq_qasm_simulator"           \
       -e MATRIX_SIZE=64                          \
       -e CIRCUIT_ID=2                            \
       -e LAYER=2                                 \
       quay.io/qiskit/qmlrun:0.0.1-z 


