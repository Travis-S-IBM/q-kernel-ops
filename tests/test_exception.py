"""Tests for exceptions functions."""
from unittest import TestCase
from src.exception import known_exception


class TestUtils(TestCase):
    """Test class for exceptions functions."""

    def test_known_exception(self):
        """Test for known_exception function."""
        error_413 = """
            Failed to run program: '413 Client Error: Payload Too Large for url:
            https://runtime-us-east.quantum-computing.ibm.com/jobs.
            <html>\\r\\n<head><title>413 Request Entity Too
            Large</title></head>\\r\\n<body>\\r\\n<center><h1>413 Request Entity Too
            Large</h1></center>\\r\\n<hr><center>nginx</center>\\r\\n</body>\\r\\n</html>\\r\\n'
        """
        tele_comment = known_exception(str(error_413))
        self.assertEqual(tele_comment, "Payload Too Large")

        error_rantoolong = """
            '("Connection broken: InvalidChunkLength(got length b\'\', 0 bytes read)",
            InvalidChunkLength(got length b\'\', 0 bytes read))'
        """
        tele_comment = known_exception(str(error_rantoolong))
        self.assertEqual(tele_comment, "Runtime: Cancelled - Ran too long")

        error_unknown = "something unusual happened !!!"
        tele_comment = known_exception(str(error_unknown))
        self.assertEqual(tele_comment, "Unknown Error")
