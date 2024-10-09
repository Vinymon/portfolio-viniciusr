import streamlit as st
import pandas as pd

def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    # Criando uma coluna combinada de 'Codigo' e 'Lote' para facilitar a seleção
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)

    return data_propostas

def format_date(df, column_name):
    # Convertendo a coluna para datetime, transformando erros em NaT
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    # Depois da conversão, formatando apenas as datas válidas para o formato desejado
    df[column_name] = df[column_name].dt.strftime('%d/%m/%Y').replace('NaT', 'Verificar Data')
    return df

def load_full_data(filename):
    data = pd.read_excel(filename)
    return data

# Carrega os dados iniciais
df_colaboradores = load_full_data('OpcoesStudioGravacoes.xlsx')
nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
id_colaboradores = df_colaboradores['IDColaborador'].unique()

def app():
    if 'df' not in st.session_state:
        st.session_state.df = load_data()
    df = load_data()

    st.title('Gerenciamento de Estoque')
    funcao_estoque = st.selectbox('Selecione uma função', ['Adicionar no estoque', 'Retirar do estoque'])

    if funcao_estoque == 'Adicionar no estoque':
        st.title('Produtos para estocar')
        df_estoque = df[df['Locale'] == 'Estoque']

        # Formatando a coluna 'DataEntrega'
        df_estoque = format_date(df_estoque, 'DataEntrega')
        df_estoque['NumeroProposta'] = df_estoque['NumeroProposta'].astype(str)
        df_estoque['Quantidade'] = df_estoque['Quantidade'].astype(int)
        df_estoque['QuantidadeSobra'] = df_estoque['QuantidadeSobra'].astype(int)
        colunas_para_exibir = ['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']
        df_estoque_selecionado = df_estoque[colunas_para_exibir]
        st.dataframe(df_estoque_selecionado)

        df_filtered_stock = st.session_state.df[st.session_state.df['Locale'] == 'Estoque']
        selected_product_stock = st.selectbox('Selecione um Produto para Estocar', df_filtered_stock['Codigo_Proposta_Lote'].unique())
        novo_locale = st.selectbox('Selecione onde enviar o produto', ['Estocado', 'Gravação', 'Manuseio', 'Expedição'])
        placeholder = st.empty()
        estoque_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password',key=1)
        if st.button('Atualizar', key=3):
            if int(estoque_id) in id_colaboradores:
                selected_code, selected_lote = selected_product_stock.split(" - ")
                condition = (st.session_state.df['Codigo'].astype(str) == selected_code) & (st.session_state.df['Lote'].astype(str) == selected_lote)
                st.session_state.df.loc[condition, 'Locale'] = novo_locale
                st.session_state.df.to_excel('Propostas.xlsx', index=False)
                estoque_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='',type='password',key=2)
                st.success('Dados atualizados com sucesso!')
            else:
                st.error('ID inválido.')

    else:
        st.title('Produtos em estoque')
        df_estocado = df[df['Locale'] == 'Estocado']

        # Formatando a coluna 'DataEntrega'
        df_estocado = format_date(df_estocado, 'DataEntrega')
        df_estocado['NumeroProposta'] = df_estocado['NumeroProposta'].astype(str)
        df_estocado['Quantidade'] = df_estocado['Quantidade'].astype(int)
        df_estocado['QuantidadeSobra'] = df_estocado['QuantidadeSobra'].astype(int)
        colunas_para_exibir = ['Nome', 'Codigo', 'NumeroProposta', 'Lote','Quantidade', 'DataEntrega', 'Vendedor', 'Cliente', 'QuantidadeSobra']
        df_estocado_selecionado = df_estocado[colunas_para_exibir]
        st.dataframe(df_estocado_selecionado)

        df_filtered_estocado = st.session_state.df[st.session_state.df['Locale'] == 'Estocado']
        selected_product_estocado = st.selectbox('Selecione um Produto para Remover do Estoque', df_filtered_estocado['Codigo_Proposta_Lote'].unique())

        placeholder = st.empty()
        estoque_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password',key=1)
        if st.button('Atualizar',key=3):
            if int(estoque_id) in id_colaboradores:
                selected_code, selected_lote = selected_product_estocado.split(" - ")
                condition = (st.session_state.df['Codigo'].astype(str) == selected_code) & (st.session_state.df['Lote'].astype(str) == selected_lote)
                st.session_state.df.loc[condition, 'Locale'] = 'Estoque'
                st.session_state.df.to_excel('Propostas.xlsx', index=False)
                st.success('Dados atualizados com sucesso!')
                estoque_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='',type='password',key=2)
            else:
                st.error('ID inválido.')