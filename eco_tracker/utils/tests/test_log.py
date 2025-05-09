import logging
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from eco_tracker.utils.log import get_logger, setup_logs_directory


def test_log_file_creation_and_content():
    """
    Test that logs are correctly created and written to a file.
    
    This test:
    1. Sets up a logger with both console and file handlers
    2. Logs messages at different levels
    3. Verifies the log file exists
    4. Verifies log messages are written to the file
    """
    # Get the logs directory
    logs_dir = setup_logs_directory()
    
    # Set up a logger
    logger = get_logger("test_file_logger")
    
    # Log some test messages
    test_debug_msg = "This is a debug message"
    test_info_msg = "This is an info message"
    test_error_msg = "This is an error message"
    
    logger.debug(test_debug_msg)
    logger.info(test_info_msg)
    logger.error(test_error_msg)
    
    # Get the log file path (it should be today's date)
    import glob
    log_files = list(logs_dir.glob("*test_file_logger.log"))
    assert len(log_files) >= 1, "No log files were created"
    
    # Verify log messages were written to the file
    with open(log_files[0], 'r') as f:
        log_content = f.read()
    
    # For debug messages to be logged, we need to set the level to DEBUG
    if logger.level <= logging.DEBUG:
        assert test_debug_msg in log_content, "Debug message not found in log file"
    assert test_info_msg in log_content, "Info message not found in log file"
    assert test_error_msg in log_content, "Error message not found in log file"


def test_setup_logs_directory():
    """Test that the logs directory is created correctly."""
    logs_dir = setup_logs_directory()
    
    # Check logs directory exists
    assert logs_dir.exists()
    assert logs_dir.is_dir()
    
    # Check logs directory is in the right place
    project_root = Path(__file__).parent.parent.parent.parent
    expected_logs_dir = project_root / "logs"
    assert logs_dir == expected_logs_dir


def test_get_logger():
    """Test that the logger is configured correctly."""
    logger = get_logger("test_logger")
    
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2
    
    # Check handler types
    handler_types = [type(h) for h in logger.handlers]
    assert logging.StreamHandler in handler_types
    assert logging.FileHandler in handler_types


def test_logger_singleton():
    """Test that the same logger instance is returned for the same name."""
    logger1 = get_logger("singleton_test")
    logger2 = get_logger("singleton_test")
    
    # Check same instance is returned
    assert logger1 is logger2
    
    # Check handlers aren't duplicated
    assert len(logger1.handlers) == 2