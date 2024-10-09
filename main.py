import streamlit as st
from paginas import me
from sistemapages import sistema

st.set_page_config(page_title='Vinicius Curriculum', page_icon= '📃',layout = 'wide')

st.sidebar.write("Hello, this is a page dedicated to showcasing a little about myself and some of the projects I've worked on. In the sidebar menu, you can choose between the page for my Resume and the page where I present my project. Thank you!")
page = st.sidebar.radio("Select a page:",['About me/ Curriculum', 'Project'])

if page == 'About me/ Curriculum':
    me.app()
if page == 'Project':
    sistema.app()