import os
import warnings
try:
    import pytest
    pytest_support = True
except ImportError:
    pytest_support = False

def RunTests():
    if pytest_support:
        test_dir = os.path.dirname(__file__)
        pytest.main([test_dir])
    else:
        warnings.warn("The pytest package has not been found. Cannot run the tests for Brian2Lava.")

if __name__ == '__main__':
    RunTests()