#!/usr/bin/python3

import matplotlib.pyplot as plt
from cvxopt import matrix, spdiag
import chompack as cp
import numpy as np
import random

from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit_machine_learning.datasets import ad_hoc_data


from qiskit.circuit.library import TwoLocal

seed = 12345
backend = Aer.get_backend('aer_simulator')


two_ex = TwoLocal(num_qubits=4,\
                  rotation_blocks=['rx','rz'],\
                  entanglement_blocks='cx',\
                  entanglement='full',\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True),\
                  initial_state=None),\
                  name='TwoLocal_example')


print (two_ex)


