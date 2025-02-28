"""Run all tests for the Manticore CockroachDB client."""

import os
import sys
import pytest
import logging
from test_utils import is_cockroachdb_running


def run_tests():
    """Run all tests."""
    # Configure logging for database connections
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check if a database is available
    if not os.environ.get("DATABASE_URL") and not is_cockroachdb_running():
        print("\033[93mWARNING: No CockroachDB instance detected!\033[0m")
        print("Tests requiring a database will be skipped.")
        print("")
        print("To run all tests, either:")
        print("1. Start a local CockroachDB instance:")
        print("   cockroach start-single-node --insecure --listen-addr=localhost --background")
        print("   or")
        print("2. Set the DATABASE_URL environment variable:")
        print("   export DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require")
        print("")
    
    # Add the parent directory to sys.path to ensure import paths work correctly
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    
    # Run the tests
    return pytest.main([
        "-xvs",  # Verbose, stop on first failure
        os.path.dirname(os.path.abspath(__file__)),  # Path to test directory
    ])


if __name__ == "__main__":
    sys.exit(run_tests()) 