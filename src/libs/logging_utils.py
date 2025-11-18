"""Logging utilities for new-python-repo.

This module provides utilities for enhanced logging functionality,
including hierarchical logger name generation for function-level tracing.
"""

import inspect
import logging
from typing import Optional, Union
from pathlib import Path

# Configure module-level logger - NO handlers, NO setLevel
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def set_logger_w_obj_name(eliminate_init: bool = False) -> logging.Logger:
    """
    Generate a hierarchical logger name based on the calling function/method.
    
    This function creates logger names that follow the pattern:
    - Function: 'module_name.function_name'
    - Method: 'module_name.ClassName.method_name'
    
    Returns:
        logging.Logger: Configured logger instance with hierarchical name
    
    Examples:
        >>> # From a standalone function
        >>> def process_data(data):
        ...     logger = set_logger_w_obj_name()
        ...     logger.info("Processing data")
        ...     # Logger name: 'my_package.utils.process_data'
        
        >>> # From a class method
        >>> class AnalyticsEngine:
        ...     def run_query(self, query):
        ...         logger = set_logger_w_obj_name()
        ...         logger.info("Running query")
        ...         # Logger name: 'my_package.analytics.AnalyticsEngine.run_query'
    
    Notes:
        - This function must be called directly from the function/method you want to track
        - Logger configuration (handlers, levels) should be done at entry points only
        - Use this for granular debugging in complex workflows
    """
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name
    module_name = frame.f_globals['__name__']
    
    # Check if called from within a class method
    if 'self' in frame.f_locals:
        class_name = frame.f_locals['self'].__class__.__name__
        if eliminate_init and function_name == '__init__':
            logger_name = f"{module_name}.{class_name}"
        else:
            logger_name = f"{module_name}.{class_name}.{function_name}"
    elif 'cls' in frame.f_locals:
        class_name = frame.f_locals['cls'].__name__
        logger_name = f"{module_name}.{class_name}.{function_name}"
    else:
        logger_name = f"{module_name}.{function_name}"

    logger.debug(f"Generated hierarchical logger name: {logger_name}")
    return logging.getLogger(logger_name)

def setup_development_logging(level: int = logging.INFO, include_timestamp: bool = True) -> None:
    """
    Setup logging configuration for development/testing environments.
    
    Args:
        level: Logging level (default: logging.INFO)
        include_timestamp: Whether to include timestamp in log format
        
    Returns:
        None
        
    Example:
        >>> setup_development_logging(level=logging.DEBUG)
        >>> # Now all loggers will output to console with DEBUG level
    """
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' if include_timestamp else '%(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[logging.StreamHandler()],
        force=True
    )
    
    # Configure package loggers
    logging.getLogger('new_python_repo').setLevel(level)
    
    # Suppress noisy third-party libraries
    logging.getLogger('streamlit').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger.info(f"Development logging configured at {logging.getLevelName(level)} level")

def setup_production_logging(log_file_path: Union[str, Path], level: int = logging.INFO) -> None:
    """
    Setup logging configuration for production environments.
    
    Args:
        log_file_path: Path to log file (str or Path object)
        level: Logging level (default: logging.INFO)
        
    Returns:
        None
        
    Example:
        >>> setup_production_logging("/var/log/app/service.log")
        >>> # Logs will go to both file and console
    """
    import sys
    
    # Ensure log directory exists
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )
    
    # Your package modules - operational level
    logging.getLogger('new_python_repo').setLevel(level)
    
    # Third-party libraries - suppress noise
    for lib in ['sqlalchemy', 'urllib3', 'requests', 'boto3', 'botocore', 'streamlit']:
        logging.getLogger(lib).setLevel(logging.WARNING)
    
    logger.info(f"Production logging configured: {log_path}")

if __name__ == "__main__":
    import sys
    import logging
    
    # Test-specific logging setup
    setup_development_logging(level=logging.DEBUG)
    
    print("Testing logging utilities...")
    
    # Test basic module logger
    logger.info("Module logger test")
    
    # Test set_logger_w_obj_name in function context
    def test_function():
        func_logger = set_logger_w_obj_name()
        func_logger.info("Function-level logger test")
        return "function test completed"
    
    # Test set_logger_w_obj_name in class context
    class TestClass:
        def test_method(self):
            method_logger = set_logger_w_obj_name()
            method_logger.info("Method-level logger test")
            return "method test completed"
        
        @classmethod
        def test_classmethod(cls):
            cls_logger = set_logger_w_obj_name()
            cls_logger.info("Class method-level logger test")
            return "classmethod test completed"
    
    # Run tests
    result1 = test_function()
    print(f"Test 1: {result1}")
    
    test_obj = TestClass()
    result2 = test_obj.test_method()
    print(f"Test 2: {result2}")
    
    result3 = TestClass.test_classmethod()
    print(f"Test 3: {result3}")
    
    print("Logging utilities testing completed")