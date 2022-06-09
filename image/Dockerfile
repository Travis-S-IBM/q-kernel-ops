FROM quay.io/qiskit/qmlbuild:0.0.4-z



ENV CIRCUIT_ID 2
ENV SHOTS 32
ENV MATRIX_SIZE 5
ENV NB_QUBITS 4
ENV LAYER 1
ENV BACKEND "ibmq_qasm_simulator"
ENV QS_TOKEN NOTHING

COPY src ./src
COPY workflow.py ./workflow.py
COPY run-kernel.sh ./run-kernel.sh
    
CMD run-kernel.sh
