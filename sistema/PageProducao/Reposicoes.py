import streamlit as st
import pandas as pd
from datetime import datetime
import os

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    # Preparando os dados conforme necessário
    if 'Locale' in data_propostas.columns:
        data_propostas['Locale'] = data_propostas['Locale'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'CQDataInicio' in data_propostas.columns:
        data_propostas['CQDataInicio'] = pd.to_datetime(data_propostas['CQDataInicio'], errors='coerce')
    if 'CQIDFinal' in data_propostas.columns:
        data_propostas['CQIDFinal'] = pd.to_datetime(data_propostas['CQIDFinal'], errors='coerce')
    return data_propostas, data_colaboradores

def salvar_reposicoes(produto_selecionado, quantidade_reposicao, df_propostas):
    # Criando um DataFrame com as informações de reposição
    df_reposicoes_novo = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].copy()
    df_reposicoes_novo['Reposicoes'] = quantidade_reposicao
    
    # Verificando se o arquivo já existe
    if os.path.exists('Reposicoes.xlsx'):
        # Lendo os dados existentes
        df_reposicoes_existente = pd.read_excel('Reposicoes.xlsx')
        # Concatenando os novos dados com os existentes
        df_reposicoes_final = pd.concat([df_reposicoes_existente, df_reposicoes_novo], ignore_index=True)
    else:
        df_reposicoes_final = df_reposicoes_novo
    
    # Salvando o DataFrame final no arquivo Excel
    df_reposicoes_final.to_excel('Reposicoes.xlsx', index=False)

def app():
    df_propostas, df_colaboradores = load_data()
    
    # Aplicando o filtro para criar df_cq
    df_cq = df_propostas[
        ~df_propostas['Locale'].isin(['Saiu para entrega','Entregue']) &
        df_propostas['Locale'].notna() &
        (df_propostas['Locale'] != '') &
        (df_propostas['StatusMaterial'] != 'Pronto')
]
    # Convertendo a coluna 'Quantidade' para numérica, dentro do escopo onde df_cq está definido
    df_cq['Quantidade'] = pd.to_numeric(df_cq['Quantidade'], errors='coerce')

    # Calculando a quantidade total depois de converter 'Quantidade' para numérico
    quantidade_total = df_cq['Nome'].shape[0]

    st.title('Gerenciamento de Reposição')
    
    if len(df_cq) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:
        # Mostrando a quantidade total no subheader
        st.subheader(f"Produtos possíveis de reposição: {quantidade_total}")
        df_cq['Quantidade'] = df_cq['Quantidade'].astype(int)
        df_cq['QuantidadeSobra'] = df_cq['QuantidadeSobra'].astype(int)
        df_cq['NumeroProposta'] = df_cq['NumeroProposta'].astype(str)
        df_cq['DataEntrega'] = pd.to_datetime(df_cq['DataEntrega'], errors='coerce').dt.strftime('%d/%m/%Y')
        st.dataframe(df_cq[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_cq['Codigo_Proposta_Lote'].unique())
        quantidade_reposicao = st.number_input('Selecione uma quantidade para reposição:', min_value= 0)

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key =1)
        colaboradores_id = df_colaboradores['IDColaborador'].unique()

        # Botão para salvar as atualizações
        if st.button('Salvar', key=3):
            if int(recebimento_id) in colaboradores_id:
                recebimento_id_int = int(recebimento_id)
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
                df_propostas.at[index, 'StatusMaterial'] = 'Pronto'
                # Salvando no arquivo original de propostas
                df_propostas.to_excel('Propostas.xlsx', index=False)  
                # Chamando a função para salvar as informações de reposição
                salvar_reposicoes(produto_selecionado, quantidade_reposicao, df_propostas)
                st.success('Informações salvas com sucesso!')
                recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='', type='password', key=2)
            else:
                st.error('ID inválido!')