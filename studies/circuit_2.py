#!/usr/bin/python3

#############################################
#
# circuit_2.py
#
# example code for configurable circuit 2 
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################

from qiskit.circuit.library import TwoLocal

######## Sim Circuit 2 ########

def circuit_2(num_qubits=4, reps=1, verbose=False):

    entangler_map = [(i, i-1) for i in range(num_qubits-1,0,-1)]

    circuit =  TwoLocal(num_qubits=num_qubits,\
                  rotation_blocks=['rx','rz'],\
                  entanglement_blocks='cx',\
                  entanglement=entangler_map,\
                  reps=reps,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_2_%d_')

    if verbose: 
        print (entangler_map)
        print (circuit.decompose())

    return circuit



