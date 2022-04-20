FROM quay.io/qiskit/qmlbuild:0.0.1-z

COPY src ./src
COPY workflow.py ./workflow.py

# set up environment
# override these at runtime with e.g.
#
# podman run -it quay.io/qiskit/qmlrun -e QS_TOKEN="your-great-big-quantum-auth-token"

ENV CIRCUIT_ID 2
ENV SHOTS 32
ENV MATRIX_SIZE 5
ENV NB_QUBITS 4
ENV LAYER 1
ENV BACKEND "ibmq_qasm_simulator"
ENV QS_TOKEN NOTHING

RUN source /root/.bashrc && cd /arrow/python && export ARROW_HOME=/usr && \
    python setup.py build_ext --build-type=release bdist_wheel && \
    python setup.py install_lib 

RUN ldconfig -v
    
CMD source /root/.bashrc &&                              \
    python workflow.py authentication                    \
           --channel="ibm_quantum"                       \
           --token="${QS_TOKEN}"                         \
           --instance="ibm-q/open/main" &&               \
    python workflow.py kernel_flow                       \
           --circuit_tpl_id=[${CIRCUIT_ID}]              \
           --width=${NB_QUBITS}                          \ 
           --layer=${LAYER}                              \ 
           --matrix_size=[${MATRIX_SIZE},${MATRIX_SIZE}] \
           --backend=${BACKEND}                          \
           --shots=${SHOTS}
         

