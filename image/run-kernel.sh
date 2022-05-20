#!/bin/bash

source /root/.bashrc 
python workflow.py authentication                        \
           --channel="ibm_quantum"                       \
           --token="${QS_TOKEN}"                         \
           --instance="ibm-q/open/main" 

python workflow.py kernel_flow                           \
           --circuit_tpl_id=[${CIRCUIT_ID}]              \
           --width=${NB_QUBITS}                          \
           --layer=${LAYER}                              \
           --matrix_size=[${MATRIX_SIZE},${MATRIX_SIZE}] \
           --backend=${BACKEND}                          \
           --shots=${SHOTS}

