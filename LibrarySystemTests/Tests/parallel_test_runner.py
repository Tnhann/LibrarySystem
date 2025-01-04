import pytest
import multiprocessing
import logging
from datetime import datetime
import os
import webbrowser

def setup_parallel_logging():
    log_directory = "parallel_test_logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_directory}/parallel_test_run_{timestamp}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_tests_in_parallel():
    setup_parallel_logging()
    logging.info("Starting parallel test execution")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"test_report_{timestamp}.html"
    
    try:
        num_processes = multiprocessing.cpu_count()
        logging.info(f"Running tests with {num_processes} processes")
        
        pytest.main([
            "-n", str(num_processes),
            "-v",
            "--html=" + report_name,
            "--self-contained-html",
            "test_library_system.py"
        ])
        
        # Test raporu tarayıcıda aç
        webbrowser.open(report_name)
        logging.info("Test execution completed, report generated")
        
    except Exception as e:
        logging.error(f"Parallel test execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_tests_in_parallel() 