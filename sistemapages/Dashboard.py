import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Carregar dados
def carregar_dados():
    return pd.read_excel('Propostas.xlsx')


def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns:
        data_propostas['Codigo_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    data_propostas['DataEntrega'] = pd.to_datetime(data_propostas['DataEntrega'], errors='coerce')
    return data_propostas


def app():

    df = carregar_dados()

    # Contagem dos valores em 'Locale'
    contagem_locale = df['Locale'].value_counts()
    contagem_recebimento = df['StatusMaterial'].value_counts()
    # Título do Dashboard
    st.title('Production dashboard')

    # Organizando os widgets em 3 colunas por linha
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header(contagem_locale.get('Quality Control', 0))
        st.write('Quality Control')

    with col2:
        st.header(contagem_locale.get('Printing', 0))
        st.write('Printing')

    with col3:
        st.header(contagem_locale.get('Handling', 0))
        st.write('Handling')

    with col4:
        st.header(contagem_locale.get('Dispatch', 0))
        st.write('Dispatch')

    st.write('---')

    df_propostas = load_data()

    today = datetime.now()

    # Definindo o início do período para o dia atual
    start_of_period = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Definindo o fim do período para 3 dias após o dia atual (incluindo o dia atual, portanto +2 dias)
    end_of_period = (datetime.now() + timedelta(days=2)).replace(hour=23, minute=59, second=59, microsecond=999999)



    print("Início do período (dia seguinte):", start_of_period)
    print("Fim do período (3 dias após hoje):", end_of_period)


    um_dia = today + timedelta(days=1)

    

    start_of_week = (datetime.now() - timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Definindo o fim da semana como 7 dias após o dia atual (não após o start_of_week ajustado)
    end_of_week = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=7)


    # Imprimindo os novos valores para verificação
    print("Início da semana ajustado para 2 dias antes:", start_of_week)
    print("Fim da semana ajustado para 7 dias após hoje:", end_of_week)

    entregas_semana = df_propostas[(df_propostas['DataEntrega'].notna()) & 
                                (df_propostas['DataEntrega'] >= start_of_week) & 
                                (df_propostas['DataEntrega'] <= end_of_week) & 
                                (df_propostas['Locale'] != 'Entregue')]

    contagem_entregas_semana = entregas_semana.shape[0]

    produtos_proximos_3_dias = df_propostas[(df_propostas['DataEntrega'].notna()) & 
                                            (df_propostas['DataEntrega'] >= start_of_period) & 
                                            (df_propostas['DataEntrega'] <= end_of_period)]

    contagem_produtos_proximos_3_dias = produtos_proximos_3_dias.shape[0]
    
    entregas_1_dia = df_propostas[(df_propostas['DataEntrega'].notna()) & 
                                (df_propostas['DataEntrega'].dt.date == um_dia.date()) & 
                                (df_propostas['Locale'] != 'Entregue')]

    
    contagem_entregas_1_dia = entregas_1_dia.shape[0]

    atrasado = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=999999)

    # Filtrando para encontrar produtos entregues até o final do dia anterior
    produtos_ate_dia_anterior = df_propostas[(df_propostas['DataEntrega'].notna()) & 
                                            (df_propostas['DataEntrega'] <= atrasado)&
                                            (df_propostas['Locale'] != 'Entregue')]

    contagem_produtos_ate_dia_anterior = produtos_ate_dia_anterior.shape[0]

    st.title('Dispatch Management')

    st.subheader(f'Backordered products: {contagem_produtos_ate_dia_anterior}')
    produtos_ate_dia_anterior['DataEntrega'] = produtos_ate_dia_anterior['DataEntrega'].dt.strftime('%d/%m/%Y')
    produtos_ate_dia_anterior['NumeroProposta'] = produtos_ate_dia_anterior['NumeroProposta'].astype(str)
    produtos_ate_dia_anterior['Quantidade'] = produtos_ate_dia_anterior['Quantidade'].astype(int)
    produtos_ate_dia_anterior['QuantidadeSobra'] = produtos_ate_dia_anterior['QuantidadeSobra'].astype(int)
    produtos_ate_dia_anterior_renomeado = produtos_ate_dia_anterior.rename(columns={
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
    st.dataframe(produtos_ate_dia_anterior_renomeado[['Product Name', 'Product Code', 'Client Name', 'Delivery date', 'Quantity', 'Leftover Quantity', 'Proposal Number', 'Locale', 'Seller', 'Lote', 'Delivery place']], use_container_width=True)

    # Linha divisória
    st.write('---')