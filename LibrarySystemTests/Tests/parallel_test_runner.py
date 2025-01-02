import pytest
import multiprocessing

def run_tests_in_parallel():
    # CPU çekirdek sayısına göre paralel test çalıştırma
    num_processes = multiprocessing.cpu_count()
    pytest.main(["-n", str(num_processes), "test_library_system.py"])

if __name__ == "__main__":
    run_tests_in_parallel() 