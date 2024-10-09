import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'ExpedicaoID' in data_propostas.columns:
        data_propostas['ExpedicaoID'] = pd.to_datetime(data_propostas['ExpedicaoID'], errors='coerce')
    return data_propostas

def app():
    df_propostas = load_data()

    df_propostas['Locale'] = df_propostas['Locale'].str.strip()

    df_expedicao = df_propostas[df_propostas['Locale'] == 'Dispatch'].copy()

    st.title('Dispatch Management')
    
    if len(df_expedicao) == 0:
        st.write('Do not have products on this stage.')
    else:
        st.subheader("Products for Dispatch")
        df_expedicao['NumeroProposta'] = df_expedicao['NumeroProposta'].astype(str)
        df_expedicao['DataEntrega'] = pd.to_datetime(df_expedicao['DataEntrega'], errors='coerce')
        df_expedicao['DataEntrega'] = df_expedicao['DataEntrega'].dt.strftime('%d/%m/%Y')
        
        df_cq_renomeado = df_expedicao.rename(columns={
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

        produto_selecionado = st.selectbox("Select a Product ('Codigo' - 'Proposta' - 'Lote'):", df_expedicao['Codigo_Proposta_Lote'].unique())

        data_expedicao = st.date_input('Dispatch date:', value=today, max_value=today, format= 'DD/MM/YYYY')
        hora_expedicao = st.time_input('Dispatch Time:')
        cod_rastreio = st.text_input('Invoice:')

        if st.button('Save', key =3):
            index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]

            df_propostas.at[index, 'DataDeSaida'] = pd.to_datetime(data_expedicao)
            df_propostas.at[index, 'HoraDeSaida'] = hora_expedicao
            df_propostas.at[index, 'Locale'] = 'Saiu para entrega'
            df_propostas.at[index, 'Rastreio'] = cod_rastreio

            df_propostas.to_excel('Propostas.xlsx', index=False)
            st.success('Data updated!')