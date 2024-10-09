import streamlit as st
import pandas as pd

# Carregar dados
def carregar_dados():
    return pd.read_excel('Propostas.xlsx')

def app():
    df = carregar_dados()

    df_cq = carregar_dados()
    
    df_gravacao = carregar_dados()

    df_manuseio = carregar_dados()

    df_expedicao = carregar_dados()

    df_estoque = carregar_dados()

    df_estocado = carregar_dados()

    df = df[df['Locale'] != 'Entregue']

    df_entregue = carregar_dados()

    df_entregue = df_entregue[df_entregue['Locale'] == 'Entregue']

    df_quantidade = len(df)



    st.title(f"Produtos em Produção: {df_quantidade}")
    df['NumeroProposta'] = df['NumeroProposta'].astype(str)
    df['DataEntrega'] = pd.to_datetime(df['DataEntrega'], errors='coerce')
    df['DataEntrega'] = df['DataEntrega'].dt.strftime('%d/%m/%Y')
    df['Quantidade'] = df['Quantidade'].astype(int)
    df['QuantidadeSobra'] = df['QuantidadeSobra'].astype(int)

    st.dataframe(df[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'StatusMaterial','NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')


    df_aguardando = df[df['StatusMaterial'] == 'Aguardando liberação']

    df_quantidade = len(df_aguardando)



    st.title(f"Produtos aguardando liberação: {df_quantidade}")
    df_aguardando['NumeroProposta'] = df_aguardando['NumeroProposta'].astype(str)
    df_aguardando['DataEntrega'] = pd.to_datetime(df_aguardando['DataEntrega'], errors='coerce')
    df_aguardando['DataEntrega'] = df_aguardando['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_aguardando['Quantidade'] = df_aguardando['Quantidade'].astype(int)
    df_aguardando['QuantidadeSobra'] = df_aguardando['QuantidadeSobra'].astype(int)

    st.dataframe(df_aguardando[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_cq = df_cq[df_cq['Locale'] == 'CQ']

    df_quantidade = len(df_cq)


    df = df[df['StatusMaterial'] == 'Pronto']

    df_quantidade = len(df)



    st.title(f"Produtos em Recebimento: {df_quantidade}")
    df['NumeroProposta'] = df['NumeroProposta'].astype(str)
    df['DataEntrega'] = pd.to_datetime(df['DataEntrega'], errors='coerce')
    df['DataEntrega'] = df['DataEntrega'].dt.strftime('%d/%m/%Y')
    df['Quantidade'] = df['Quantidade'].astype(int)
    df['QuantidadeSobra'] = df['QuantidadeSobra'].astype(int)

    st.dataframe(df[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_cq = df_cq[df_cq['Locale'] == 'CQ']

    df_quantidade = len(df_cq)



    st.title(f"Produtos em CQ: {df_quantidade}")
    df_cq['NumeroProposta'] = df_cq['NumeroProposta'].astype(str)
    df_cq['DataEntrega'] = pd.to_datetime(df_cq['DataEntrega'], errors='coerce')
    df_cq['DataEntrega'] = df_cq['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_cq['Quantidade'] = df_cq['Quantidade'].astype(int)
    df_cq['QuantidadeSobra'] = df_cq['QuantidadeSobra'].astype(int)

    st.dataframe(df_cq[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_gravacao = df_gravacao[df_gravacao['Locale'] == 'Gravação']

    df_quantidade = len(df_gravacao)



    st.title(f"Produtos em Gravação: {df_quantidade}")
    df_gravacao['NumeroProposta'] = df_gravacao['NumeroProposta'].astype(str)
    df_gravacao['DataEntrega'] = pd.to_datetime(df_gravacao['DataEntrega'], errors='coerce')
    df_gravacao['DataEntrega'] = df_gravacao['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_gravacao['Quantidade'] = df_gravacao['Quantidade'].astype(int)
    df_gravacao['QuantidadeSobra'] = df_gravacao['QuantidadeSobra'].astype(int)

    st.dataframe(df_gravacao[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_manuseio = df_manuseio[df_manuseio['Locale'] == 'Manuseio']

    df_quantidade = len(df_manuseio)



    st.title(f"Produtos em Manuseio: {df_quantidade}")
    df_manuseio['NumeroProposta'] = df_manuseio['NumeroProposta'].astype(str)
    df_manuseio['DataEntrega'] = pd.to_datetime(df_manuseio['DataEntrega'], errors='coerce')
    df_manuseio['DataEntrega'] = df_manuseio['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_manuseio['Quantidade'] = df_manuseio['Quantidade'].astype(int)
    df_manuseio['QuantidadeSobra'] = df_manuseio['QuantidadeSobra'].astype(int)

    st.dataframe(df_manuseio[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_expedicao = df_expedicao[df_expedicao['Locale'] == 'Expedição']

    df_quantidade = len(df_expedicao)

    st.title(f"Produtos em Expedição: {df_quantidade}")
    df_expedicao['NumeroProposta'] = df_expedicao['NumeroProposta'].astype(str)
    df_expedicao['DataEntrega'] = pd.to_datetime(df_expedicao['DataEntrega'], errors='coerce')
    df_expedicao['DataEntrega'] = df_expedicao['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_expedicao['Quantidade'] = df_expedicao['Quantidade'].astype(int)
    df_expedicao['QuantidadeSobra'] = df_expedicao['QuantidadeSobra'].astype(int)

    st.dataframe(df_expedicao[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_estoque = df_estoque[df_estoque['Locale'] == 'Estoque']

    df_quantidade = len(df_estoque)

    st.title(f"Produtos para serem estocados: {df_quantidade}")
    df_estoque['NumeroProposta'] = df_estoque['NumeroProposta'].astype(str)
    df_estoque['DataEntrega'] = pd.to_datetime(df_estoque['DataEntrega'], errors='coerce')
    df_estoque['DataEntrega'] = df_estoque['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_estoque['Quantidade'] = df_estoque['Quantidade'].astype(int)
    df_estoque['QuantidadeSobra'] = df_estoque['QuantidadeSobra'].astype(int)

    st.dataframe(df_estoque[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_estocado = df_estocado[df_estocado['Locale'] == 'Estocado']

    df_quantidade = len(df_estocado)

    st.title(f"Produtos estocados: {df_quantidade}")
    df_estocado['NumeroProposta'] = df_estocado['NumeroProposta'].astype(str)
    df_estocado['DataEntrega'] = pd.to_datetime(df_estocado['DataEntrega'], errors='coerce')
    df_estocado['DataEntrega'] = df_estocado['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_estocado['Quantidade'] = df_estocado['Quantidade'].astype(int)
    df_estocado['QuantidadeSobra'] = df_estocado['QuantidadeSobra'].astype(int)

    st.dataframe(df_estocado[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')

    df_entregue = df_entregue[df_entregue['Locale'] == 'Entregue']

    df_quantidade = len(df_entregue)

    st.title(f"Produtos Entregues: {df_quantidade}")
    df_entregue['NumeroProposta'] = df_entregue['NumeroProposta'].astype(str)
    df_entregue['DataEntrega'] = pd.to_datetime(df_entregue['DataEntrega'], errors='coerce')
    df_entregue['DataEntrega'] = df_entregue['DataEntrega'].dt.strftime('%d/%m/%Y')
    df_entregue['Quantidade'] = df_entregue['Quantidade'].astype(int)
    df_entregue['QuantidadeSobra'] = df_entregue['QuantidadeSobra'].astype(int)

    st.dataframe(df_entregue[['Locale', 'Nome', 'Codigo', 'Quantidade','QuantidadeSobra','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'OPStatus','NotaStatus','Tipo','Lote']], use_container_width=True)

    st.write('---')