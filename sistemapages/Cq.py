import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    # Preparando os dados conforme necessário
    if 'CQStatus' in data_propostas.columns:
        data_propostas['CQStatus'] = data_propostas['CQStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'CQDataInicio' in data_propostas.columns:
        data_propostas['CQDataInicio'] = pd.to_datetime(data_propostas['CQDataInicio'], errors='coerce')
    if 'CQIDFinal' in data_propostas.columns:
        data_propostas['CQIDFinal'] = pd.to_datetime(data_propostas['CQIDFinal'], errors='coerce')
    return data_propostas

def app():
    df_propostas = load_data()
    
    # Filtrando vendedores com propostas em CQ
    df_cq = df_propostas[(df_propostas['StatusMaterial'] == 'Recebido') & ~(df_propostas['CQStatus'].isin(['Quality Control Completed']))].copy()
    
    st.title('Quality Control Management')
    
    if len(df_cq) == 0:
        st.write('Do not have products on this stage.')
    else:

        st.subheader("Products for Quality Control")

        df_cq['DataEntrega'] = pd.to_datetime(df_cq['DataEntrega'], errors='coerce')
        df_cq['DataEntrega'] = df_cq['DataEntrega'].dt.strftime('%d/%m/%Y')
        df_cq['NumeroProposta'] = df_cq['NumeroProposta'].astype(str)
        df_cq['Quantidade'] = df_cq['Quantidade'].astype(int)
        df_cq['QuantidadeSobra'] = df_cq['QuantidadeSobra'].astype(int)

        # Renomeando as colunas
        df_cq_renomeado = df_cq.rename(columns={
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

        # Exibindo o DataFrame renomeado
        st.dataframe(df_cq_renomeado[['Product Name', 'Product Code', 'Client Name', 'Delivery date', 'Quantity', 'Leftover Quantity', 'Proposal Number', 'Locale', 'Seller', 'Lote', 'Delivery place']], use_container_width=True)

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Select a Product ('Product Code' - 'Proposal Number' - 'Lote'):", df_cq['Codigo_Proposta_Lote'].unique())
        produto_info = df_cq[df_cq['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        # Determinar as opções disponíveis baseadas no status atual do produto
        if produto_info['CQStatus'] == 'Quality Control Started':
            status_options = ['Quality Control Completed']
        else:
            status_options = ['Quality Control Started']

        # Atualização do Status do Material com opções condicionais
        new_status = st.selectbox("Quality Control Status", status_options)

        if new_status == 'Quality Control Started':
            # Atualização de datas
            data_cq = st.date_input('Start Date:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'Quality Control Completed':
            # Atualização de datas
            data_cq = st.date_input('End Date:', value=today, max_value=today, format= 'DD/MM/YYYY')
            prox_etapa = ('Printing')
        # Campo de ID com senha para confirmação


        # Botão para salvar as atualizações
        if st.button('Save', key =3):
            index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
            if new_status == 'Quality Control Started':
                df_propostas.at[index, 'CQStatus'] = new_status
                df_propostas.at[index, 'CQDataInicio'] = pd.to_datetime(data_cq)
            else:
                df_propostas.at[index, 'CQStatus'] = new_status
                df_propostas.at[index, 'Locale'] = prox_etapa
                df_propostas.at[index, 'CQDataFinal'] = pd.to_datetime(data_cq)
                
            df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
            st.success('Data updated!')