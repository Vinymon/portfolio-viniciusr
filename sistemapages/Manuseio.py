import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    if 'ManuseioStatus' in data_propostas.columns:
        data_propostas['ManuseioStatus'] = data_propostas['ManuseioStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'ManuseioDataInicio' in data_propostas.columns:
        data_propostas['ManuseioDataInicio'] = pd.to_datetime(data_propostas['ManuseioDataInicio'], errors='coerce')
    if 'ManuseioInicioID' in data_propostas.columns:
        data_propostas['ManuseioInicioID'] = pd.to_datetime(data_propostas['ManuseioInicioID'], errors='coerce')
    return data_propostas

def app():
    df_propostas = load_data()
    
    df_manuseio = df_propostas[(df_propostas['Locale'] == 'Handling')].copy()
    
    st.title('Handling Management')
    
    if len(df_manuseio) == 0:
        st.write('Do not have products on this stage.')
    else:

        st.subheader("Products for Management")
        df_manuseio['NumeroProposta'] = df_manuseio['NumeroProposta'].astype(str)
        df_manuseio['Quantidade'] = df_manuseio['Quantidade'].astype(int)
        df_manuseio['QuantidadeSobra'] = df_manuseio['QuantidadeSobra'].astype(int)
        df_manuseio['DataEntrega'] = pd.to_datetime(df_manuseio['DataEntrega'], errors='coerce')
        df_manuseio['DataEntrega'] = df_manuseio['DataEntrega'].dt.strftime('%d/%m/%Y')
        
        df_cq_renomeado = df_manuseio.rename(columns={
            'Nome': 'Product Name',
            'Codigo': 'Product Code',
            'Cliente': 'Client Name',
            'DataEntrega': 'Delivery date',
            'Quantidade': 'Quantity',
            'QuantidadeSobra': 'Leftover Quantity',
            'NumeroProposta': 'Proposal Number',
            'Locale': 'Locale',
            'Vendedor': 'Seller',
            'Lote': 'Lote',
            'LocalEntrega': 'Delivery place'
        })

        st.dataframe(df_cq_renomeado[['Product Name', 'Product Code', 'Client Name', 'Delivery date', 'Quantity', 'Leftover Quantity', 'Proposal Number', 'Locale', 'Seller', 'Lote', 'Delivery place']], use_container_width=True)
        st.write("---")

        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_manuseio['Codigo_Proposta_Lote'].unique())
        produto_info = df_manuseio[df_manuseio['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        if produto_info['ManuseioStatus'] == 'Handling Started':
            status_options = ['Handling Completed']
        else:
            status_options = ['Handling Started']

        new_status = st.selectbox("Handling Status", status_options)

        if new_status == 'Handling Started':
            data_cq = st.date_input('Start Date:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'Handling Completed':

            nota_status = 'Pendente'
            data_cq = st.date_input('End Date:', value=today, max_value=today, format= 'DD/MM/YYYY')

        prox_etapa = 'Dispatch'

        if st.button('Save', key =3):
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
                if new_status == 'Handling Started':
                    df_propostas.at[index, 'ManuseioStatus'] = new_status
                    df_propostas.at[index, 'ManuseioDataInicio'] = pd.to_datetime(data_cq)
                else:          
                    df_propostas.at[index, 'ManuseioStatus'] = new_status
                    df_propostas.at[index, 'Locale'] = prox_etapa
                    df_propostas.at[index, 'ManuseioDataFinal'] = pd.to_datetime(data_cq)
                    df_propostas.at[index, 'NotaStatus'] = nota_status
                df_propostas.to_excel('Propostas.xlsx', index=False)
                st.success('Data updated!')