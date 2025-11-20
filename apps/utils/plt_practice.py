
import streamlit as st
from pathlib import Path



st.title('Live matplotlib Practice')
st.markdown('This App demonstrates live plotting with matplotlib in Streamlit. With this capability, you can create any figure even interactive visualizations on the fly.')

# Get the directory where this file is located
current_dir = Path(__file__).parent
image_path = current_dir / "milly.jpg"

st.image(str(image_path), caption='Milly was painting', width=600)

# st.write("For example, these inquality are quite useful in decision science, but it is possible that most of people do not know what is the use of them in practice. With the help of a live demo App, it will be very easy to demonstrate those knowledge from textbooks. So just memorize them first, and I might let you know what is the use of them when I have a chance.")
# st.latex(
#     r'''\text{Markov's inequality: }\;\; P(x>c)\leq\frac{E[X]}{c}\\
#     \text{Chebyshev's inequality: }\;\;\;\; P(|X-E[X]| \geq k)\leq\frac{Var[X]}{k^2}\\
#     \text{Jensen's inequality: }\;\;\;\;\;\; E[g(X)]\geq g(E[X]), \text{if } g \text{ is convex}
#     '''
# )

# Display a subheader and provide a text area for users to enter Python code
st.subheader('The following section is a simple tool for you to inteact with Streamlit, you can easily plot our first figure in seconds. Just like Miss Milly, don\'t hesitate too much but just do it!!') 

smile='''
import matplotlib.pyplot as plt
from numpy import linspace
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(1,1,1, aspect=1)
ax.scatter([0.5],[0.5], c='#FFCC00', s=60000, label='face')
ax.scatter([0.35, 0.65],[0.63, 0.63], c='k', s=1000, label='eyes')

X = linspace(0.3, 0.7, 100)
Y = 2*(X-0.5)**2 + 0.3

ax.plot(X, Y, c='k', linewidth=8, label='smile')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
'''

code = st.text_area('Enter your code in the following text area and see the result immediately!', 'st.text("Hello World! Do something with a big smile!!")' + smile, height=250)
st.button('run')

# Execute the code entered by the user in the local context
local_vars = locals()
exec(code, local_vars)

# Create columns for layout and display the plot if fig exists
if 'fig' in local_vars:
    _,col2,_ = st.columns([2,6,2])
    with col2:
        st.pyplot(local_vars['fig'])