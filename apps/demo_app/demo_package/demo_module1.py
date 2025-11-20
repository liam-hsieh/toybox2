
"""Example module demonstrating package-based imports.

This module is part of the libs package and shows how to organize
reusable code in a proper Python package structure. It implements
comprehensive logging following Python best practices.

Features:
    - Module-level logging configuration
    - Function-level logging with context
    - Error handling with detailed logging
    - Module testing with configurable log levels

Example:
    >>> import logging
    >>> logging.basicConfig(level=logging.INFO)
    >>> from libs.example_module1 import import_checking1
    >>> result = import_checking1("test")
    INFO:libs.example_module1:Processing import check with input: test...
"""

import logging

# Configure module-level logger - NO handlers, NO setLevel
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def import_checking1(test_str: str) -> str:
    """Check if package import is working correctly.
    
    This function demonstrates that the libs package can be imported
    successfully and provides a simple way to test the import system.
    
    Args:
        test_str: A test string to echo back with confirmation message
        
    Returns:
        A formatted string confirming successful import with the input string
        
    Example:
        >>> import_checking1("Hello World!")
        'Import import_checking1 successful, and here is your input: Hello World!'
    """
    logger.info(f"Processing import check with input: {test_str[:50]}...")
    result = f"Import import_checking1 successful, and here is your input: {test_str}"
    logger.debug(f"Generated result: {result[:100]}...")
    return result

def calculate_sum(numbers: list[float]) -> float:
    """Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of numbers to sum
        
    Returns:
        The sum of all numbers in the list
        
    Raises:
        TypeError: If input is not a list
        ValueError: If list contains non-numeric values
        
    Example:
        >>> calculate_sum([1, 2, 3, 4, 5])
        15.0
    """
    logger.debug(f"Calculating sum for {len(numbers) if isinstance(numbers, list) else 'non-list'} items")
    
    if not isinstance(numbers, list):
        logger.error("Input validation failed: input is not a list")
        raise TypeError("Input must be a list")
    
    try:
        result = float(sum(numbers))
        logger.info(f"Sum calculation completed: {len(numbers)} numbers, result={result}")
        return result
    except (TypeError, ValueError) as e:
        logger.error(f"Sum calculation failed: {e}")
        raise ValueError("All items in list must be numeric") from e

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
    print("Testing example_module1 functions...")
    
    # Test import_checking1
    test_result1 = import_checking1("Hello from module test!")
    print(f"Test 1 Result: {test_result1}")
    
    # Test calculate_sum with valid input
    test_numbers = [1, 2, 3, 4, 5]
    sum_result = calculate_sum(test_numbers)
    print(f"Test 2 Result: Sum of {test_numbers} = {sum_result}")
    
    # Test error handling
    try:
        calculate_sum("not a list")
    except TypeError as e:
        print(f"Test 3 Result: Correctly caught error - {e}")
    
    print("Module testing completed")

def format_message(message: str, prefix: str = "INFO") -> str:
    """Format a message with a prefix.
    
    Args:
        message: The message content to format
        prefix: Prefix to add (default: "INFO")
        
    Returns:
        Formatted message string
        
    Example:
        >>> format_message("Processing complete", "SUCCESS")
        'SUCCESS: Processing complete'
    """
    return f"{prefix}: {message}"