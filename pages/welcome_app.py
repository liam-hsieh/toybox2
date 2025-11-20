import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from socket import gethostname
#from os import chdir, getcwd,path
import os
from send_mail import send_mail
# Disable Streamlit's warning about using pyplot in a global way
#st.set_option('deprecation.showPyplotGlobalUse', False)

# Define the folder name and get the current working directory
folder = '(---select a project first---)_st'
path = os.path.abspath(os.getcwd())
for_VM = False

# Check if there are any directories with '_st' in the current directory
# If so, change the working directory to the specified folder
if any(map(lambda i: '_st' in i, os.listdir(path))):
    for_VM = True
    os.chdir(folder)


#st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

# https://hsdes-api.intel.com/rest/user/lhsieh
# default is same as https://hsdes-api.intel.com/rest/user/lhsieh?expand=personal
# using groups could check AGS roles

st.title('Welcome to the E2E Solutions Station')
st.header('A tool collections built for supporting IAO SCM projects by E2E Solutions team')

st.subheader('Everything here :red[was built at ZERO additional cost to the cost center]; just available resources for Blue Badges and Liam Hsieh\'s time only!!')

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
st.image("./The Analytics Platform.png")

# Display a subheader and a text input for users to leave a message
st.subheader("Leave a message for the system administrator")
message = st.text_area("Enter your message here:", placeholder="Type your message...")

# Button to submit the message
if st.button("Send Message"):
    if message.strip():
        # Send the message using the send_mail function
        try:
            send_mail(st.session_state["cookie_dict"], message)

            st.success("Your message has been sent successfully!")
        except Exception as e:
            st.error(f"Failed to send the message. Error: {e}")
    else:
        st.warning("Please enter a message before sending.")


#st.markdown('This portal is for idea illustration and/or prototypes demonstration;some tutorials with program scripts may also be found. \n More details such like methedologies behind them may refer to posts on my site [Personal website](http://liamhsieh.info)')
#st.image(image, caption='Milly was painting', use_column_width=True)

# st.write("For example, these inquality are quite useful in decision science, but it is possible that most of people do not know what is the use of them in practice. With the help of a live demo App, it will be very easy to demonstrate those knowledge from textbooks. So just memorize them first, and I might let you know what is the use of them when I have a chance.")
# st.latex(
#     r'''\text{Markov's inequality: }\;\; P(x>c)\leq\frac{E[X]}{c}\\
#     \text{Chebyshev's inequality: }\;\;\;\; P(|X-E[X]| \geq k)\leq\frac{Var[X]}{k^2}\\
#     \text{Jensen's inequality: }\;\;\;\;\;\; E[g(X)]\geq g(E[X]), \text{if } g \text{ is convex}
#     '''
# )

# Display a subheader and provide a text area for users to enter Python code
# st.subheader('The following section is a simple tool for you to inteact with Streamlit, you can easily plot our first figure in seconds. Just like Miss Milly, don\'t hesitate too much but just do it!!') 

# smile='''
# fig = plt.figure(figsize=(5,5))
# ax = fig.add_subplot(1,1,1, aspect=1)
# ax.scatter([0.5],[0.5], c='#FFCC00', s=60000, label='face')
# ax.scatter([0.35, 0.65],[0.63, 0.63], c='k', s=1000, label='eyes')

# X = np.linspace(0.3, 0.7, 100)
# Y = 2*(X-0.5)**2 + 0.3

# ax.plot(X, Y, c='k', linewidth=8, label='smile')

# ax.set_xlim(0, 1)
# ax.set_ylim(0, 1)

# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.set_xticks([])
# ax.set_yticks([])
# '''

# code = st.text_area('Enter your code in the following text area and see the result immediately!', 'st.text("Hello World! Do something with a big smile!!")' + smile, height=250)
# st.button('run')
# # Execute the code entered by the user in the local context
# exec(code, locals())

# # Create columns for layout and display the plot in the middle column
# _,col2,_ = st.columns([2,6,2])
# with col2:
#     st.pyplot(fig)

# If the script changed the working directory for a VM, change it back to the parent directory
if for_VM: os.chdir('../')



