"""Tests for circuits."""
from unittest import TestCase
from qiskit import QuantumCircuit

from src.circuits import circuit_2, circuit_5, kernel_circuit


class TestUtils(TestCase):
    """Test class for circuits functions."""

    def test_circuit_2(self):
        """Test to test the circuit template 5."""
        circuit = circuit_2()
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_circuit_5(self):
        """Test to test the circuit template 5."""
        circuit = circuit_5(width=3, layer=1)
        self.assertTrue(isinstance(circuit, QuantumCircuit))

    def test_kernel_circuit(self):
        """Test to test the kernel circuit."""
        circuit_tpl = circuit_5()
        kernel_cirq = kernel_circuit(circuit_tpl, 42, 4242)
        self.assertTrue(isinstance(kernel_cirq, QuantumCircuit))
