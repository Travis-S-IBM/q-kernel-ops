"""Tests for circuits."""
from unittest import TestCase
from qiskit import QuantumCircuit

from src.circuits import circuit_5


class TestUtils(TestCase):
    """Test class for circuits functions."""

    def test_circuit_5(self):
        circuit = circuit_5(width=3, layer=1, seed1=12)
        self.assertTrue(isinstance(circuit, QuantumCircuit))
