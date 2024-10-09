import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    # Preparando os dados conforme necessário
    if 'CQStatus' in data_propostas.columns:
        data_propostas['CQStatus'] = data_propostas['CQStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'CQDataInicio' in data_propostas.columns:
        data_propostas['CQDataInicio'] = pd.to_datetime(data_propostas['CQDataInicio'], errors='coerce')
    if 'CQIDFinal' in data_propostas.columns:
        data_propostas['CQIDFinal'] = pd.to_datetime(data_propostas['CQIDFinal'], errors='coerce')
    return data_propostas, data_colaboradores

def app():
    df_propostas, df_colaboradores = load_data()
    
    # Filtrando vendedores com propostas em CQ
    df_cq = df_propostas[(df_propostas['StatusMaterial'] == 'Recebido') & ~(df_propostas['CQStatus'].isin(['CQ Finalizado']))].copy()
    
    st.title('Gerenciamento de CQ')
    
    if len(df_cq) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:

        st.subheader("Produtos para CQ")

        df_cq['DataEntrega'] = pd.to_datetime(df_cq['DataEntrega'], errors='coerce')
        df_cq['DataEntrega'] = df_cq['DataEntrega'].dt.strftime('%d/%m/%Y')
        df_cq['NumeroProposta'] = df_cq['NumeroProposta'].astype(str)
        df_cq['Quantidade'] = df_cq['Quantidade'].astype(int)
        df_cq['QuantidadeSobra'] = df_cq['QuantidadeSobra'].astype(int)
        st.dataframe(df_cq[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_cq['Codigo_Proposta_Lote'].unique())
        produto_info = df_cq[df_cq['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        # Determinar as opções disponíveis baseadas no status atual do produto
        if produto_info['CQStatus'] == 'CQ Iniciado':
            status_options = ['CQ Finalizado']
        else:
            status_options = ['CQ Iniciado']

        # Atualização do Status do Material com opções condicionais
        new_status = st.selectbox("Status do CQ", status_options)

        if new_status == 'CQ Iniciado':
            # Seleção do Responsável e Data de Início
            nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
            responsavel_selecionado = st.selectbox('Selecione o Responsável:', nome_colaboradores)

            # Atualização de datas
            data_cq = st.date_input('Data de Início:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'CQ Finalizado':
            # Atualização de datas
            data_cq = st.date_input('Data de Finalização:', value=today, max_value=today, format= 'DD/MM/YYYY')
            prox_etapa = st.selectbox('Selecione a próxima etapa:', ['Gravação', 'Manuseio', 'Estoque'])

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key =1)
        colaboradores_id = df_colaboradores['IDColaborador'].unique()

        # Botão para salvar as atualizações
        if st.button('Salvar', key =3):
            if int(recebimento_id) in colaboradores_id:
                recebimento_id_int = int(recebimento_id)
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
                if new_status == 'CQ Iniciado':
                    df_propostas.at[index, 'CQStatus'] = new_status
                    df_propostas.at[index, 'CQResponsavel'] = responsavel_selecionado
                    df_propostas.at[index, 'CQDataInicio'] = pd.to_datetime(data_cq)
                    df_propostas.at[index, 'CQIDInicio'] = recebimento_id_int
                else:
                    df_propostas.at[index, 'CQStatus'] = new_status
                    df_propostas.at[index, 'Locale'] = prox_etapa
                    df_propostas.at[index, 'CQDataFinal'] = pd.to_datetime(data_cq)
                    df_propostas.at[index, 'CQIDFinal'] = recebimento_id_int
                df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
                st.success('Informações salvas com sucesso!')
                recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='', type='password', key =2)
            else:
                st.error('ID inválido!')