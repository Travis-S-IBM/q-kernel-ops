#!/bin/bash

cd /opt/experiments/q-kernel-ops/resources/kernel_metadata

python workflow.py authentication --channel="ibm_quantum" --token="${QS_TOKEN}" --instance="ibm-q/open/main"

./gen_data.sh

