#!/usr/bin/python3

#############################################
#
# TwoLocal_example.py
#
# example code for a sampling of circuit types 
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################

from qiskit.circuit.library import TwoLocal
from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit import Parameter

######## Sim Circuit 2 ########

entangler_map = [(3,2),(2,1),(1,0)]

sim_circuit = {}

sim_circuit['2'] =  TwoLocal(num_qubits=4,\
                  rotation_blocks=['rx','rz'],\
                  entanglement_blocks='cx',\
                  entanglement=entangler_map,\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_2')

print (sim_circuit['2'].decompose())

######## Sim Circuit 3 ########

sim_circuit['3']= TwoLocal(num_qubits=4,\
                  rotation_blocks=['rx','rz'],\
                  entanglement_blocks='crz',\
                  entanglement=entangler_map,\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_3')

print (sim_circuit['3'].decompose())

######## Sim Circuit 14 ########

entangler_map = [(3,0),(2,3),(1,2),(0,1)]

sim_circuit['14'] = TwoLocal(num_qubits=4,\
                  rotation_blocks='ry',\
                  entanglement_blocks='crx',\
                  entanglement=entangler_map,\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_14')

#print (sim_circuit['14'].decompose())

entangler_map = [(3,2),(0,3),(1,0),(2,1)]

sim_circuit['14'].barrier ()

sim_circuit['14'] += TwoLocal(num_qubits=4,\
                  rotation_blocks='ry',\
                  entanglement_blocks='crx',\
                  entanglement=entangler_map,\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θa',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_14a')

print (sim_circuit['14'].decompose())

######## Sim Circuit 9 ########

sim_circuit['9'] = QuantumCircuit(4)

for i in range(4): sim_circuit['9'].h(i)

sim_circuit['9'].barrier()

sim_circuit['9'].cz(3,2)
sim_circuit['9'].cz(2,1)
sim_circuit['9'].cz(1,0)

sim_circuit['9'].barrier()

for i in range(4):                       
    ThetaString ='θ['+str(i)+']'
    theta = Parameter(ThetaString)
    sim_circuit['9'].rx(theta,i)

print (sim_circuit['9'])


######## Sim Circuit 18 ########

entangler_map = [(3,0),(2,3),(1,2),(0,1)]

sim_circuit['18'] = TwoLocal(num_qubits=4,\
                  rotation_blocks=['rx','rz'],\
                  entanglement_blocks='crz',\
                  entanglement=entangler_map,\
                  reps=1,\
                  skip_unentangled_qubits=False,\
                  skip_final_rotation_layer=True,\
                  parameter_prefix='θ',\
                  insert_barriers=True,\
                  initial_state=None,\
                  name='sim_circuit_14')

print (sim_circuit['18'].decompose())
