import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    # Preparando os dados conforme necessário
    if 'GravacaoStatus' in data_propostas.columns:
        data_propostas['GravacaoStatus'] = data_propostas['GravacaoStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'GravacaoDataInicio' in data_propostas.columns:
        data_propostas['GravacaoDataInicio'] = pd.to_datetime(data_propostas['GravacaoDataInicio'], errors='coerce')
    if 'GravacaoIDFinal' in data_propostas.columns:
        data_propostas['GravacaoIDFinal'] = pd.to_datetime(data_propostas['GravacaoIDFinal'], errors='coerce')
    return data_propostas

def app():
    df_propostas = load_data()
    
    # Filtrando vendedores com propostas em Gravação
    df_gravacao = df_propostas[(df_propostas['Locale'] == 'Printing')].copy()
    
    st.title('Printing Management')
    
    if len(df_gravacao) == 0:
        st.write('Do not have products on this stage.')
    else:

        st.subheader("Products for printing")
        df_gravacao['DataEntrega'] = pd.to_datetime(df_gravacao['DataEntrega'], errors='coerce')
        df_gravacao['DataEntrega'] = df_gravacao['DataEntrega'].dt.strftime('%d/%m/%Y')
        df_gravacao['NumeroProposta'] = df_gravacao['NumeroProposta'].astype(str)
        df_gravacao['Quantidade'] = df_gravacao['Quantidade'].astype(int)
        df_gravacao['QuantidadeSobra'] = df_gravacao['QuantidadeSobra'].astype(int)

        df_cq_renomeado = df_gravacao.rename(columns={
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

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Select a Product ('Product Code' - 'Proposal Number' - 'Lote'):", df_gravacao['Codigo_Proposta_Lote'].unique())
        produto_info = df_gravacao[df_gravacao['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        # Determinar as opções disponíveis baseadas no status atual do produto
        if produto_info['GravacaoStatus'] == 'Printing Started':
            status_options = ['Printing Completed']
        else:
            status_options = ['Printing Started']

        # Atualização do Status do Material com opções condicionais
        new_status = st.selectbox("Printing Status", status_options)

        if new_status == 'Printing Started':
            # Atualização de datas
            data_cq = st.date_input('Start Date:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'Printing Completed':
            # Atualização de datas
            data_cq = st.date_input('End Date:', value=today, max_value=today, format= 'DD/MM/YYYY')
            prox_etapa = ('Handling')
        # Botão para salvar as atualizações
        if st.button('Save', key =3):
            index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
            if new_status == 'Printing Started':
                df_propostas.at[index, 'GravacaoStatus'] = new_status
                df_propostas.at[index, 'GravacaoDataInicio'] = pd.to_datetime(data_cq)
            else:
                df_propostas.at[index, 'GravacaoStatus'] = new_status
                df_propostas.at[index, 'Locale'] = prox_etapa
                df_propostas.at[index, 'GravacaoDataInicio'] = pd.to_datetime(data_cq)
                
            df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
            st.success('Data updated!')