import pytest
import sys
import os

# Ensure the project directory is in the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

def run_all_tests():
    """
    Run all pytest tests for views, serializers, and models.
    """
    # Define the paths to test files
    test_files = [
        'apps/gold_online_store/tests/test_api_views.py',
        'apps/gold_online_store/tests/test_serializers.py',
        'apps/gold_online_store/tests/test_models.py',
    ]

    # Run pytest with verbose output and coverage
    exit_code = pytest.main([
        '-v',  # Verbose output
        '--cov=apps',  # Measure coverage for the 'apps' directory
        '--cov-report=html',  # Generate HTML coverage report
        '--cov-report=term',  # Generate terminal coverage report
    ] + test_files)

    return exit_code

if __name__ == '__main__':
    print("Starting test execution...")
    exit_code = run_all_tests()
    if exit_code == 0:
        print("All tests passed successfully!")
    else:
        print(f"Test execution completed with exit code {exit_code}. Some tests may have failed.")
    sys.exit(exit_code)