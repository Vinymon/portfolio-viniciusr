import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    # Preparando os dados conforme necessário
    if 'ManuseioStatus' in data_propostas.columns:
        data_propostas['ManuseioStatus'] = data_propostas['ManuseioStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'ManuseioDataInicio' in data_propostas.columns:
        data_propostas['ManuseioDataInicio'] = pd.to_datetime(data_propostas['ManuseioDataInicio'], errors='coerce')
    if 'ManuseioInicioID' in data_propostas.columns:
        data_propostas['ManuseioInicioID'] = pd.to_datetime(data_propostas['ManuseioInicioID'], errors='coerce')
    return data_propostas, data_colaboradores

def app():
    df_propostas, df_colaboradores = load_data()
    
    # Filtrando vendedores com propostas em CQ
    df_manuseio = df_propostas[(df_propostas['Locale'] == 'Manuseio')].copy()
    
    st.title('Gerenciamento de Manuseio')
    
    if len(df_manuseio) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:

        st.subheader("Produtos para Manuseio")
        df_manuseio['NumeroProposta'] = df_manuseio['NumeroProposta'].astype(str)
        df_manuseio['Quantidade'] = df_manuseio['Quantidade'].astype(int)
        df_manuseio['QuantidadeSobra'] = df_manuseio['QuantidadeSobra'].astype(int)
        df_manuseio['DataEntrega'] = pd.to_datetime(df_manuseio['DataEntrega'], errors='coerce')
        df_manuseio['DataEntrega'] = df_manuseio['DataEntrega'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_manuseio[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_manuseio['Codigo_Proposta_Lote'].unique())
        produto_info = df_manuseio[df_manuseio['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        # Determinar as opções disponíveis baseadas no status atual do produto
        if produto_info['ManuseioStatus'] == 'Manuseio Iniciado':
            status_options = ['Manuseio Finalizado']
        else:
            status_options = ['Manuseio Iniciado']

        # Atualização do Status do Material com opções condicionais
        new_status = st.selectbox("Status do Manuseio", status_options)

        if new_status == 'Manuseio Iniciado':
                # Seleção do Responsável e Data de Início
            nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
            responsavel_selecionado = st.selectbox('Selecione o Responsável:', nome_colaboradores)
            data_cq = st.date_input('Data de Início:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'Manuseio Finalizado':
            # Atualização de datas
            nota_status = 'Pendente'
            data_cq = st.date_input('Data de Finalização:', value=today, max_value=today, format= 'DD/MM/YYYY')
            prox_etapa = st.selectbox('Selecione a próxima etapa:', ['Solicitação NF', 'Estoque'])

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        manuseio_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key =1)
        colaboradores_id = df_colaboradores['IDColaborador'].unique()

        # Botão para salvar as atualizações
        if st.button('Salvar', key =3):
            if int(manuseio_id) in colaboradores_id:
                manuseio_id_int = int(manuseio_id)
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
                if new_status == 'Manuseio Iniciado':
                    df_propostas.at[index, 'ManuseioStatus'] = new_status
                    df_propostas.at[index, 'ManuseioResponsavel'] = responsavel_selecionado
                    df_propostas.at[index, 'ManuseioDataInicio'] = pd.to_datetime(data_cq)
                    df_propostas.at[index, 'ManuseioInicioID'] = manuseio_id_int
                else:          
                    df_propostas.at[index, 'ManuseioStatus'] = new_status
                    df_propostas.at[index, 'Locale'] = prox_etapa
                    df_propostas.at[index, 'ManuseioDataFinal'] = pd.to_datetime(data_cq)
                    df_propostas.at[index, 'ManuseioFinalID'] = manuseio_id_int
                    df_propostas.at[index, 'NotaStatus'] = nota_status
                df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
                st.success('Informações salvas com sucesso!')
                manuseio_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='', type='password', key =2)
            else:
                st.error('ID inválido!')