"""Tests for the TestRunner class"""

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from invenio_et_probo.test_runner import TestRunner

class TestRunnerTests(unittest.TestCase):
    def setUp(self):
        self.runner = TestRunner()
        
    def test_should_exclude(self):
        """Test exclude pattern matching"""
        self.runner.exclude_patterns = ["test_skip_*", "integration_*"]
        
        # Should exclude
        self.assertTrue(self.runner.should_exclude("test_skip_this"))
        self.assertTrue(self.runner.should_exclude("integration_test"))
        
        # Should not exclude
        self.assertFalse(self.runner.should_exclude("test_normal"))
        self.assertFalse(self.runner.should_exclude("unit_test"))
        
    @patch('multiprocessing.Process')
    def test_run_tests_timeout(self, mock_process):
        """Test handling of test execution timeout"""
        # Mock process that doesn't finish
        mock_process_instance = MagicMock()
        mock_process_instance.is_alive.return_value = True
        mock_process.return_value = mock_process_instance
        
        # Run tests
        result = self.runner.run_tests(Path("."))
        
        # Verify timeout handling
        self.assertIn('error', result)
        self.assertIn('timeout', result['error'].lower())
        mock_process_instance.terminate.assert_called_once()
        
    def test_format_error(self):
        """Test error formatting"""
        try:
            raise ValueError("Test error")
        except ValueError as e:
            formatted = self.runner._format_error(self, (type(e), e, e.__traceback__))
            
        self.assertIn("ValueError", formatted)
        self.assertIn("Test error", formatted)
        self.assertIn("test_runner_test.py", formatted)
