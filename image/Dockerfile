FROM quay.io/qiskit/qmlbuild:0.0.0-z

COPY src ./src
COPY worflow.py ./worflow.py

# set up environment

ARG CIRCUIT_ID=2
ARG SHOTS=32
ARG MATRIX_SIZE=5
ARG NB_QUBITS=4
ARG LAYER=1
ARG BACKEND=ibm_qasm_simulator
ARG QS_TOKEN=NOTHING
    
CMD python worflow.py authentication --auth="legacy" --token="${QS_TOKEN}" --instance="ibm-q/open/main" && \
    python worflow.py kernel_flow --circuit_tpl_id=[${CIRCUIT_ID}] --width=${NB_QUBITS} --layer=${LAYER} --matrix_size=[${MATRIX_SIZE},${MATRIX_SIZE}] --backend="${BACKEND}" --shots=${SHOTS}
         

