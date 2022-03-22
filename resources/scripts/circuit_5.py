#!/usr/bin/python3

#############################################
#
# circuit_5.py
#
# example code for configurable circuit 5
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################

from qiskit.circuit.library import TwoLocal
from qiskit.utils import algorithm_globals


def circuit_2(width=4, layer=1, seed1=42, verbose=False):
    nb_qubits = width
    repetitions = layer
    algorithm_globals.random_seed = seed1

    rotation_blocks = ['rx', 'rz']
    entanglement_blocks = 'crz'

    entangler_map = []
    for i in range(nb_qubits):
        for u in range(nb_qubits):
            if u != i:
                entangler_map.append((i, u))

    entanglement = entangler_map
    insert_barriers = True
    skip_final_rotation_layer = False

    circuit = TwoLocal(num_qubits=nb_qubits,
                       rotation_blocks=rotation_blocks,
                       entanglement_blocks=entanglement_blocks,
                       entanglement=entanglement,
                       reps=repetitions,
                       insert_barriers=insert_barriers,
                       skip_final_rotation_layer=skip_final_rotation_layer)
    circuit.measure_all()

    if verbose:
        print(entangler_map)
        print(circuit.decompose())

    return circuit
