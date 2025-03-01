"""Test runner for imitatio_ostendendi."""

import unittest
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import all test cases
from test_base_widget import TestWidget
from test_text_widget import TestText
from test_entry_widget import TestEntry
from test_button_widget import TestButton
from test_frame_widget import TestFrame, TestLabelFrame

def run_tests():
    """Run all test cases."""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWidget))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestText))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEntry))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestButton))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFrame))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLabelFrame))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
