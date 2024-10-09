import streamlit as st
import pandas as pd
from sistemapages import details, Cq, Dashboard, Expedicao, Manuseio, Gravacao

def app():
    page = st.sidebar.radio("Select a page:", ['Project Details','Dashboard', 'Quality Control', 'Printing', 'Handling', 'Dispatch'])
    if st.sidebar.button('Reset data'):

        dados_backup = pd.read_excel('PropostasBackup.xlsx')
        
        dados_backup.to_excel('Propostas.xlsx', index=False)
        
        st.sidebar.success('Success!')
    if page == 'Project Details':
        details.app()
    if page == 'Dashboard':
        Dashboard.app()
    if page == 'Quality Control':
        Cq.app()
    if page == 'Printing':
        Gravacao.app()
    if page == 'Handling':
        Manuseio.app()
    if page == 'Dispatch':
        Expedicao.app()