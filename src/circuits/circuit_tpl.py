"""
#############################################
#
# circuit_tpl.py
#
# Template for circuits
#
#
#############################################
"""

from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit


def twolocal_tpl(
    nb_qubits: int,
    repetitions: int,
    rotation_blocks: [str],
    entanglement_blocks: str,
    entanglement,
    skip_final_rotation_layer: bool,
    name="Circuit_tpl",
    verbose=False,
) -> QuantumCircuit:
    """Template TwoLocal circuit

    Args:
        nb_qubits: number of qubits
        repetitions: number of repetitions
        rotation_blocks: base gate block init rotation
        entanglement_blocks: base gate block for entanglement
        entanglement: way for entanglement map or linear, circular, full
        skip_final_rotation_layer: having the rotation_blocks at the end
        name: circuit name
        verbose: True/False

    Return:
        The TwoLocal circuit generate
    """
    circuit = TwoLocal(
        num_qubits=nb_qubits,
        rotation_blocks=rotation_blocks,
        entanglement_blocks=entanglement_blocks,
        entanglement=entanglement,
        reps=repetitions,
        insert_barriers=False,
        skip_final_rotation_layer=skip_final_rotation_layer,
        name=name,
    )

    if verbose:
        print(circuit.decompose())

    return circuit
