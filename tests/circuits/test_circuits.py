"""Tests for circuits."""
from unittest import TestCase
from qiskit import QuantumCircuit

from src.circuits import (
    circuit_2,
    circuit_5,
    circuit_10,
    circuit_18,
    kernel_circuit,
    twolocal_tpl,
)


class TestUtils(TestCase):
    """Test class for circuits functions."""

    def test_circuit_2(self):
        """Test to test the circuit template 2."""
        circuit = circuit_2()
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_circuit_5(self):
        """Test to test the circuit template 5."""
        circuit = circuit_5(width=3, layer=1)
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_circuit_10(self):
        """Test to test the circuit template 10."""
        circuit = circuit_10(width=3, layer=2, verbose=True)
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_circuit_18(self):
        """Test to test the circuit template 18."""
        circuit = circuit_18(verbose=True)
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_kernel_circuit(self):
        """Test to test the kernel circuit."""
        circuit_tpl = circuit_5()
        kernel_cirq = kernel_circuit(circuit_tpl, 42, 4242)
        self.assertTrue(isinstance(kernel_cirq, QuantumCircuit))

    def test_twolocal(self):
        """Test to test the kernel circuit."""
        twolocal_circuit = twolocal_tpl(
            nb_qubits=5,
            repetitions=1,
            rotation_blocks=["rx", "rz"],
            entanglement_blocks="cx",
            entanglement="full",
            skip_final_rotation_layer=True,
            verbose=False,
        )
        self.assertTrue(isinstance(twolocal_circuit, QuantumCircuit))
