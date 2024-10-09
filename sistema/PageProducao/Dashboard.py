import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Carregar dados
def carregar_dados():
    return pd.read_excel('Propostas.xlsx')


def load_data():
    data_propostas = pd.read_excel('propostas.xlsx')
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
    st.title('Dashboard de Produção')

    # Organizando os widgets em 3 colunas por linha
    col1, col2, col3 = st.columns(3)
    with col1:
        pronto_count = contagem_recebimento.get('Pronto', 0)
        atrasado_count = contagem_recebimento.get('Atrasado', 0)
        total_count = pronto_count + atrasado_count

        st.header(total_count)
        st.write('Recebimento')

    with col2:
        st.header(contagem_locale.get('CQ', 0))
        st.write('Controle de Qualidade')

    with col3:
        st.header(contagem_locale.get('Estoque', 0))
        st.write('Estoque')

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header(contagem_locale.get('Gravação', 0))
        st.write('Gravação')

    with col5:
        st.header(contagem_locale.get('Manuseio', 0))
        st.write('Manuseio')

    with col6:
        st.header(contagem_locale.get('Expedição', 0))
        st.write('Expedição')

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

    st.title('Gerenciamento de Entrega')

    st.subheader(f'Produtos em atraso: {contagem_produtos_ate_dia_anterior}')
    produtos_ate_dia_anterior['DataEntrega'] = produtos_ate_dia_anterior['DataEntrega'].dt.strftime('%d/%m/%Y')
    produtos_ate_dia_anterior['NumeroProposta'] = produtos_ate_dia_anterior['NumeroProposta'].astype(str)
    produtos_ate_dia_anterior['Quantidade'] = produtos_ate_dia_anterior['Quantidade'].astype(int)
    produtos_ate_dia_anterior['QuantidadeSobra'] = produtos_ate_dia_anterior['QuantidadeSobra'].astype(int)
    st.dataframe(produtos_ate_dia_anterior[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
    st.write('---')

    # Produtos a serem entregues esta semana
    st.subheader(f'Produtos a serem entregues nos próximos 7 dias: {contagem_entregas_semana}')
    entregas_semana['DataEntrega'] = entregas_semana['DataEntrega'].dt.strftime('%d/%m/%Y')
    entregas_semana['NumeroProposta'] = entregas_semana['NumeroProposta'].astype(str)
    entregas_semana['Quantidade'] = entregas_semana['Quantidade'].astype(int)
    entregas_semana['QuantidadeSobra'] = entregas_semana['QuantidadeSobra'].astype(int)
    st.dataframe(entregas_semana[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
    st.write('---')

    # Produtos a serem entregues nos próximos 3 dias
    st.subheader(f'Produtos a serem entregues nos próximos 3 dias: {contagem_produtos_proximos_3_dias}')
    produtos_proximos_3_dias['DataEntrega'] = produtos_proximos_3_dias['DataEntrega'].dt.strftime('%d/%m/%Y')
    produtos_proximos_3_dias['NumeroProposta'] = produtos_proximos_3_dias['NumeroProposta'].astype(str)
    produtos_proximos_3_dias['Quantidade'] = produtos_proximos_3_dias['Quantidade'].astype(int)
    produtos_proximos_3_dias['QuantidadeSobra'] = produtos_proximos_3_dias['QuantidadeSobra'].astype(int)
    st.dataframe(produtos_proximos_3_dias[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
    st.write('---')

    # Produtos a serem entregues no próximo dia
    st.subheader(f'Produtos a serem entregues no próximo dia: {contagem_entregas_1_dia}')
    entregas_1_dia['DataEntrega'] = entregas_1_dia['DataEntrega'].dt.strftime('%d/%m/%Y')
    entregas_1_dia['NumeroProposta'] = entregas_1_dia['NumeroProposta'].astype(str)
    entregas_1_dia['Quantidade'] = entregas_1_dia['Quantidade'].astype(int)
    entregas_1_dia['QuantidadeSobra'] = entregas_1_dia['QuantidadeSobra'].astype(int)
    st.dataframe(entregas_1_dia[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
    st.write('---')