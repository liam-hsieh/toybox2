"""Streamlit demo application showcasing package-based imports.

This demo application demonstrates the package-based import pattern
using the libs.example_module1 module. It includes comprehensive
logging configuration for Streamlit applications.

Features:
    - Package-based imports from libs/ directory
    - Streamlit logging configuration
    - Interactive string processing
    - Number calculation with error handling
    - Third-party library log suppression

Usage:
    uv run streamlit run src/demo_app.py --server.port 8521

Author: New Python Repo Template
"""

import streamlit as st
import logging
# it will work if the repo is installed as a package by uv
from libs.example_module1 import import_checking1, calculate_sum

# Configure logging for Streamlit app (only if not already configured)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Set levels for different components
    logging.getLogger('new_python_repo').setLevel(logging.INFO)
    logging.getLogger('streamlit').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Demo App", layout="wide")

st.title("Demo Streamlit App - Package Import")
st.write("Testing package-based imports from libs.example_module1")

logger.info("Demo app started - package import mode")

# Input section
st.subheader("String Processing")
user_input = st.text_input("Enter something to check:")

# Process with import_checking1
if user_input:
    st.subheader("Result")
    logger.info(f"Processing user input: {user_input[:50]}...")
    result = import_checking1(user_input)
    st.write(result)
    st.success("Processing completed successfully")
else:
    st.info("Enter text above to see results")

# Number calculation section
st.subheader("Number Calculation")
st.write("Test the calculate_sum function from example_module1")

numbers_input = st.text_input("Enter numbers separated by commas (e.g., 1,2,3,4,5):")

if numbers_input:
    try:
        # Parse numbers
        numbers = [float(x.strip()) for x in numbers_input.split(',')]
        logger.info(f"Calculating sum for {len(numbers)} numbers")
        
        result = calculate_sum(numbers)
        st.write(f"**Sum:** {result}")
        st.write(f"**Count:** {len(numbers)} numbers")
        st.success("Calculation completed")
        
    except ValueError as e:
        logger.error(f"Input parsing error: {e}")
        st.error("Please enter valid numbers separated by commas")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Powered by Streamlit")