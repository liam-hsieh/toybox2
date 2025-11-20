
"""Example module demonstrating direct imports.

This module shows how to organize utility functions that are imported
directly from the same directory, without package structure. It implements
advanced logging features including hierarchical logger names.

Features:
    - Module-level and function-level logging
    - Hierarchical logger names using set_logger_w_obj_name()
    - Class-based logging demonstrations
    - Input validation with detailed logging
    - Text analysis with processing metrics

Example:
    >>> import logging
    >>> logging.basicConfig(level=logging.INFO)
    >>> from example_module2 import import_checking2
    >>> result = import_checking2("test")
    INFO:example_module2:Processing direct import check with input: test...
"""

import logging
from datetime import datetime
from typing import Dict, Any
from libs.logging_utils import set_logger_w_obj_name

# Configure module-level logger - NO handlers, NO setLevel
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def import_checking2(test_str: str) -> str:
    """Check if direct import is working correctly.
    
    This function demonstrates that modules can be imported directly
    from the same directory without package structure.
    
    Args:
        test_str: A test string to echo back with confirmation message
        
    Returns:
        A formatted string confirming successful import with the input string
        
    Example:
        >>> import_checking2("Hello World")
        'Import import_checking2 successful, and here is your input: Hello World'
    """
    logger.info(f"Processing direct import check with input: {test_str[:50]}...")
    result = f"Import import_checking2 successful, and here is your input: {test_str}"
    logger.debug(f"Generated result: {result[:100]}...")
    return result

def process_text(text: str) -> Dict[str, Any]:
    """Process text and return analysis information.
    
    Args:
        text: The text string to analyze
        
    Returns:
        Dictionary containing text analysis results including:
        - word_count: Number of words
        - char_count: Number of characters
        - processed_at: Timestamp of processing
        
    Example:
        >>> result = process_text("Hello world")
        >>> result['word_count']
        2
    """
    logger.debug(f"Processing text analysis for {len(text)} characters")
    words = text.split()
    
    result = {
        "word_count": len(words),
        "char_count": len(text),
        "processed_at": datetime.now().isoformat(),
        "original_text": text
    }
    
    logger.info(f"Text analysis completed: {len(words)} words, {len(text)} characters")
    return result

def validate_input(value: str, min_length: int = 1) -> bool:
    """Validate input string meets minimum requirements.
    
    Args:
        value: String to validate
        min_length: Minimum required length (default: 1)
        
    Returns:
        True if validation passes, False otherwise
        
    Example:
        >>> validate_input("test", 3)
        True
        >>> validate_input("hi", 3)
        False
    """
    logger.debug(f"Validating input: type={type(value).__name__}, length={len(value) if isinstance(value, str) else 'N/A'}, min_length={min_length}")
    
    is_valid = isinstance(value, str) and len(value.strip()) >= min_length
    
    if is_valid:
        logger.debug("Input validation passed")
    else:
        logger.warning(f"Input validation failed: {'not string' if not isinstance(value, str) else f'length {len(value.strip())} < {min_length}'}")
    
    return is_valid

class ExampleClass:
    """Example class demonstrating class-based logging patterns.
    
    This class showcases different approaches to logging within class methods:
    - Instance-level logger initialization
    - Method-level hierarchical logging
    - Comparison of different logging approaches
    
    Attributes:
        logger: Instance-level logger with class context
        
    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> obj = ExampleClass()
        >>> result = obj.example_method("test data")
        INFO:example_module2.ExampleClass.example_method:Example logging by method logger...
        INFO:example_module2.ExampleClass:Example logging by instance logger...
    """
    def __init__(self):
        """Initialize ExampleClass with instance-level logger.
        
        The instance logger uses set_logger_w_obj_name() with eliminate_init=True
        to create a logger named after the class rather than the __init__ method.
        """
        # Initialize logger for this instance
        self.logger = set_logger_w_obj_name(eliminate_init=True)
    def example_method(self, param: str) -> str:
        """Demonstrate different logging approaches within a class method.
        
        This method shows two different logging patterns:
        1. Method-level logger: Creates hierarchical name (module.Class.method)
        2. Instance-level logger: Uses the class-level logger initialized in __init__
        
        Args:
            param: A string parameter to process
            
        Returns:
            A confirmation string with the processed parameter
            
        Example:
            >>> obj = ExampleClass()
            >>> result = obj.example_method("test input")
            'Method executed with param: test input'
            
        Note:
            The method demonstrates both logging approaches to show the difference
            in logger naming and context. In production, choose one consistent approach.
        """
        logger = set_logger_w_obj_name()
        # Note that logger and self.logger would be different, depends on how details you want to log
        logger.info(f"Example logging by `method logger` - Executing example_method with param: {param[:50]}...")
        self.logger.info(f"Example logging by `instance logger` - Executing example_method with param: {param[:50]}...")

        return f"Method executed with param: {param}"
    
if __name__ == "__main__":
    import sys
    import logging  # Import logging for test execution
    
    # Test-specific logging (terminal only, configurable level)
    logging.basicConfig(
        level=logging.DEBUG,  # Change to INFO/WARNING as needed
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )
    
    # Fine-tune specific loggers for debugging
    logging.getLogger('new_python_repo').setLevel(logging.DEBUG)
    
    # Test execution
    print("Testing example_module2 functions...")
    
    # Test import_checking2
    test_result1 = import_checking2("Hello from direct import test!")
    print(f"Test 1 Result: {test_result1}")
    
    # Test process_text
    test_text = "This is a sample text for analysis with multiple words."
    analysis_result = process_text(test_text)
    print(f"Test 2 Result: Text analysis - {analysis_result}")
    
    # Test validate_input
    valid_tests = [
        ("valid text", 5, True),
        ("short", 10, False),
        ("", 1, False),
        (123, 1, False)  # Non-string input
    ]
    
    for i, (text, min_len, expected) in enumerate(valid_tests, 3):
        result = validate_input(text, min_len)
        status = "✓" if result == expected else "✗"
        print(f"Test {i} Result: {status} validate_input({repr(text)}, {min_len}) = {result}")
    
    print("Module testing completed")

    ec = ExampleClass()
    ec.example_method("Testing example method logging")