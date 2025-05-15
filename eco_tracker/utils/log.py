import logging
import os
import sys
from datetime import datetime
from pathlib import Path


# Ensure logs directory exists in project root
def setup_logs_directory():
    """Create logs directory if it doesn't exist."""
    project_root = Path(__file__).parent.parent.parent
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir

def get_logger(name="log", log_level=logging.INFO):
    """
    Configure and return a logger that outputs to both console and a log file.
    
    Args:
        name (str, optional): Logger name. If None, returns the root logger.
        log_level (int, optional): Logging level. Defaults to logging.INFO.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Skip if logger is already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(log_level)
    logs_dir = setup_logs_directory()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create file handler
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = f"{timestamp}_{name}.log"
    file_handler = logging.FileHandler(logs_dir / log_filename, encoding='utf-8')
    file_handler.setLevel(log_level)
    
    # Create formatters
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    
    # Set formatters
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

