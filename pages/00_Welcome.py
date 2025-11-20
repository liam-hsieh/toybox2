import streamlit as st
import matplotlib.pyplot as plt
from numpy import linspace
from pathlib import Path

from shared.components import create_sidebar_footer
from shared.send_mail import send_mail

# Get the directory where this file is located
current_dir = Path(__file__).parent

# Add sidebar footer
create_sidebar_footer()


with open("README.md", "r") as f:
    st.markdown(f.read())

# Message input
message = st.text_area("Enter your message:")

# Button to submit the message
if st.button("Send Message"):
    if message.strip():
        # Send the message using the send_mail function
        try:
            send_mail(st.session_state.current_user, message)

            st.success("Your message has been sent successfully!")
        except Exception as e:
            st.error(f"Failed to send the message. Error: {e}")
    else:
        st.warning("Please enter a message before sending.")

