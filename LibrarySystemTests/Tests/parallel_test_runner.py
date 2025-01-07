import pytest
import multiprocessing

def run_tests():
    pytest.main([
        "test_library_system.py::TestLibrarySystem::test_all_features",
        "-v",
        "-s",
        "--capture=no",
        "-n", str(multiprocessing.cpu_count()),
        "--dist=loadfile"
    ])

if __name__ == "__main__":
    run_tests() 