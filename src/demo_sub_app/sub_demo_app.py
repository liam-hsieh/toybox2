"""Streamlit demo application showcasing direct module imports.

This demo application demonstrates the direct import pattern using
modules from the same directory. It includes advanced logging features
and comprehensive text analysis capabilities.

Features:
    - Direct imports from same directory
    - Hierarchical logging with set_logger_w_obj_name()
    - Interactive text analysis
    - Input validation with detailed feedback
    - Class method logging demonstrations

Usage:
    uv run streamlit run src/demo_sub_app/sub_demo_app.py --server.port 8521

Author: New Python Repo Template
"""

import streamlit as st
import logging
# it will work if the repo is installed as a package by uv
from example_module2 import import_checking2, process_text, validate_input


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

st.set_page_config(page_title="Demo Sub App", layout="wide")

st.title("Demo Streamlit App - Direct Import")
st.write("Testing direct imports from example_module2")

logger.info("Demo sub app started - direct import mode")

# Input section
st.subheader("String Processing")
user_input = st.text_input("Enter something to check:")

# Process with import_checking2
if user_input:
    st.subheader("Import Check Result")
    logger.info(f"Processing user input: {user_input[:50]}...")
    result = import_checking2(user_input)
    st.write(result)
    st.success("Import check completed")
else:
    st.info("Enter text above to see results")

# Text analysis section
st.subheader("Text Analysis")
analysis_text = st.text_area("Enter text to analyze:", height=100)

if analysis_text:
    logger.info(f"Starting text analysis for {len(analysis_text)} characters")
    
    # Validate input
    is_valid = validate_input(analysis_text, min_length=1)
    
    if is_valid:
        analysis_result = process_text(analysis_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Word Count", analysis_result["word_count"])
            st.metric("Character Count", analysis_result["char_count"])
        
        with col2:
            st.write("**Processed At:**")
            st.write(analysis_result["processed_at"])
        
        st.success("Text analysis completed")
    else:
        st.error("Input validation failed")
else:
    st.info("Enter text above to analyze")

# Footer
st.divider()
st.caption("Powered by Streamlit")