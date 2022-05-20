FROM quay.io/qiskit/qmlbuild:0.0.1-z

COPY src ./src
COPY workflow.py ./workflow.py

# set up environment
# override these at runtime with e.g.
#
# podman run -it quay.io/qiskit/qmlrun:0.0.2-z -e QS_TOKEN="your-great-big-quantum-auth-token"

ENV CIRCUIT_ID 2
ENV SHOTS 32
ENV MATRIX_SIZE 5
ENV NB_QUBITS 4
ENV LAYER 1
ENV BACKEND "ibmq_qasm_simulator"
ENV QS_TOKEN NOTHING

RUN ldconfig -v

COPY run-kernel.sh ./run-kernel.sh
    
CMD run-kernel.sh
