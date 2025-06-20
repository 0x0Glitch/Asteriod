#!/usr/bin/env python3
"""
Test runner for the Asteroids game.
Runs all tests and provides detailed reporting.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_entities import TestEntities
from tests.test_systems import TestGameState, TestCollisionSystem, TestInputSystem


class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result class with colored output."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
        self.verbosity = verbosity  # Store verbosity explicitly
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            self.stream.write(f"\033[92m✓ {test._testMethodName}\033[0m\n")
        else:
            self.stream.write("\033[92m.\033[0m")
        self.stream.flush()
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            self.stream.write(f"\033[91m✗ {test._testMethodName} (ERROR)\033[0m\n")
        else:
            self.stream.write("\033[91mE\033[0m")
        self.stream.flush()
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            self.stream.write(f"\033[91m✗ {test._testMethodName} (FAIL)\033[0m\n")
        else:
            self.stream.write("\033[91mF\033[0m")
        self.stream.flush()
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.verbosity > 1:
            self.stream.write(f"\033[93m- {test._testMethodName} (SKIP: {reason})\033[0m\n")
        else:
            self.stream.write("\033[93mS\033[0m")
        self.stream.flush()


class AsteroidsTestRunner:
    """Custom test runner for the Asteroids game."""
    
    def __init__(self, verbosity=2):
        self.verbosity = verbosity
        self.start_time = None
        self.end_time = None
        
    def run_all_tests(self):
        """Run all test suites."""
        print("🚀 Starting Asteroids Game Test Suite")
        print("=" * 50)
        
        self.start_time = time.time()
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add test cases
        test_classes = [
            TestEntities,
            TestGameState,
            TestCollisionSystem,
            TestInputSystem
        ]
        
        for test_class in test_classes:
            tests = loader.loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        
        # Run tests
        runner = unittest.TextTestRunner(
            stream=sys.stdout,
            verbosity=self.verbosity,
            resultclass=ColoredTextTestResult
        )
        
        result = runner.run(suite)
        
        self.end_time = time.time()
        
        # Print summary
        self.print_summary(result)
        
        return result.wasSuccessful()
    
    def print_summary(self, result):
        """Print test summary."""
        duration = self.end_time - self.start_time
        
        print("\n" + "=" * 50)
        print("🎯 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = result.testsRun
        successes = getattr(result, 'success_count', total_tests - len(result.failures) - len(result.errors))
        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped)
        
        print(f"Total Tests: {total_tests}")
        print(f"\033[92m✓ Passed: {successes}\033[0m")
        
        if failures > 0:
            print(f"\033[91m✗ Failed: {failures}\033[0m")
        
        if errors > 0:
            print(f"\033[91m⚠ Errors: {errors}\033[0m")
        
        if skipped > 0:
            print(f"\033[93m- Skipped: {skipped}\033[0m")
        
        print(f"Duration: {duration:.2f}s")
        
        if result.wasSuccessful():
            print("\n\033[92m🎉 ALL TESTS PASSED! 🎉\033[0m")
            print("The game is ready for production! 🚀")
        else:
            print("\n\033[91m❌ SOME TESTS FAILED\033[0m")
            print("Please fix the issues before deploying.")
            
            if result.failures:
                print("\n\033[91mFAILURES:\033[0m")
                for test, traceback in result.failures:
                    print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
            
            if result.errors:
                print("\n\033[91mERRORS:\033[0m")
                for test, traceback in result.errors:
                    error_msg = traceback.split('\\n')[-2] if '\\n' in traceback else traceback
                    print(f"- {test}: {error_msg}")
    
    def run_specific_test(self, test_name):
        """Run a specific test by name."""
        print(f"🎯 Running specific test: {test_name}")
        print("=" * 50)
        
        self.start_time = time.time()
        
        # Try to find and run the specific test
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        try:
            # Load specific test
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test_name))
        except Exception as e:
            print(f"\033[91mError loading test '{test_name}': {e}\033[0m")
            return False
        
        # Run test
        runner = unittest.TextTestRunner(
            stream=sys.stdout,
            verbosity=self.verbosity,
            resultclass=ColoredTextTestResult
        )
        
        result = runner.run(suite)
        
        self.end_time = time.time()
        self.print_summary(result)
        
        return result.wasSuccessful()


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Asteroids Game Test Runner")
    parser.add_argument(
        "--test", 
        help="Run a specific test (e.g., tests.test_entities.TestEntities.test_player_creation)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="count", 
        default=2,
        help="Increase verbosity level"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output"
    )
    
    args = parser.parse_args()
    
    verbosity = 0 if args.quiet else args.verbose
    
    runner = AsteroidsTestRunner(verbosity=verbosity)
    
    try:
        if args.test:
            success = runner.run_specific_test(args.test)
        else:
            success = runner.run_all_tests()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\033[93m⚠ Tests interrupted by user\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\n\033[91m❌ Test runner error: {e}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main() 