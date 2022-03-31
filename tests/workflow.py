"""Tests for CLI commands."""
import pandas as pd
from unittest import TestCase
from src.workflow import Workflow


class TestUtils(TestCase):
    """Test class for Workflow cli."""

    def test_view_kernel(self):
        """Test to test the view kernel command."""
        data_file = Workflow.view_kernel(file_name="kernels-2-ideal.csv")
        self.assertTrue(isinstance(data_file, pd.DataFrame))
