import streamlit as st
import matplotlib.pyplot as plt
from numpy import linspace
from pathlib import Path

from shared.components import create_sidebar_footer
from shared.send_mail import send_mail

# Get the directory where this file is located
current_dir = Path(__file__).parent


st.title('Welcome to the E2E Solutions Station')
st.header('A tool collections built for supporting IAO SCM projects by E2E Solutions team')

st.subheader('Everything here :red[was built at ZERO additional cost to the cost center]; just available resources for Blue Badges and Liam Hsieh\'s time only!!')

# Add sidebar footer
create_sidebar_footer()

st.markdown(
"""
Now we got:  
- **DataBroker**: A RESTful API service set as a foundation of most applications/tools
- **DataPrep**: The supporting tool for data preparation of setting up BY data; a standalone environment [DEV](https://e2esol-test.intel.com:8052/) is for dev/test purpose  
- **Snow Dumper**: A tool for dumping solving results with Python data manipulation libraries 

, and these only for Solutions team:
- **Account Manager**: A lightweight system for managing user permission among tools
- **SQL Pipeline Editor/Tester**: App for Managing/Creating SQL pipelines
- **Snowflake Proxy**: Base functionality to support programatic approach with data from Snowflake

We also serve few services which might be not for you if you have never heard about them:  
- **[DevHub](https://e2esol.intel.com/jupyterhub)**: Remote multi-users notebook environment; multiple languages supported such as Python, C/C++, R, Julia, Fortran.
- **[Voilà](https://e2esol.intel.com/voila)**: The collection for prototypes/proof-of-concept; also allow rendering notebook in JupyterHub for rapid prototyping.
- **[Plotly Dash](https://e2esol.intel.com/dash)**: The collection for interactive web applications.
- [**R-Studio Server**](https://liamhsieh.amr.corp.intel.com/rstudio): Based on R Version 4.1.2
- [liamhsieh-toolbox](https://pypi.org/project/liamhsieh-toolbox/): A Python utility collection which is utilized by most projects.

We also use a [Sharepoint site](https://intel.sharepoint.com/sites/bydataprep) to enable seamless integration across our services and applications. This site acts as a central hub for collaboration, document sharing, and workflow management, leveraging the flexibility and capabilities of Office 365 to streamline project coordination and resource access for all users.

For those projects are in progress and/or under developement, may visit [Liam's Website](https://liamhsieh.intel.com/) to have more details.

"""
)


st.subheader("All these tools and applications sit on top of our analytics platform, which is illustrated below")
image_path = current_dir / "The Analytics Platform.png"
st.image(image_path)

# Display a subheader and a text input for users to leave a message
st.subheader("Leave a message for the system administrator")
message = st.text_area("Enter your message here:", placeholder="Type your message...")

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

