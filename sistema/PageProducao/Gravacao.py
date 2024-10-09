import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    data_gravadores = pd.read_excel('OpcoesGravadores.xlsx')
    # Preparando os dados conforme necessário
    if 'GravacaoStatus' in data_propostas.columns:
        data_propostas['GravacaoStatus'] = data_propostas['GravacaoStatus'].astype(object)
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'GravacaoDataInicio' in data_propostas.columns:
        data_propostas['GravacaoDataInicio'] = pd.to_datetime(data_propostas['GravacaoDataInicio'], errors='coerce')
    if 'GravacaoIDFinal' in data_propostas.columns:
        data_propostas['GravacaoIDFinal'] = pd.to_datetime(data_propostas['GravacaoIDFinal'], errors='coerce')
    return data_propostas, data_colaboradores, data_gravadores

def app():
    df_propostas, df_colaboradores, df_gravadores= load_data()
    
    # Filtrando vendedores com propostas em Gravação
    df_gravacao = df_propostas[(df_propostas['Locale'] == 'Gravação')].copy()
    
    st.title('Gerenciamento de Gravação')
    
    if len(df_gravacao) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:

        st.subheader("Produtos para Gravação")
        df_gravacao['NumeroProposta'] = df_gravacao['NumeroProposta'].astype(str)
        df_gravacao['Quantidade'] = df_gravacao['Quantidade'].astype(int)
        df_gravacao['QuantidadeSobra'] = df_gravacao['QuantidadeSobra'].astype(int)
        df_gravacao['DataEntrega'] = pd.to_datetime(df_gravacao['DataEntrega'], errors='coerce')
        df_gravacao['DataEntrega'] = df_gravacao['DataEntrega'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_gravacao[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_gravacao['Codigo_Proposta_Lote'].unique())
        produto_info = df_gravacao[df_gravacao['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]

        # Determinar as opções disponíveis baseadas no status atual do produto
        if produto_info['GravacaoStatus'] == 'Gravação Iniciada':
            status_options = ['Gravação Finalizada']
        else:
            status_options = ['Gravação Iniciada']

        # Atualização do Status do Material com opções condicionais
        new_status = st.selectbox("Status da Gravação", status_options)

        if new_status == 'Gravação Iniciada':
            # Obter a lista de nomes dos gravadores únicos para o dropdown
            nome_gravadores = df_gravadores['NomeGravador'].unique()
            # Dropdown para que o usuário selecione um gravador
            gravador_selecionado = st.selectbox('Selecione o Gravador:', nome_gravadores)

            # Verificar se o gravador selecionado é 'Studio Gravações' e proceder com lógica específica
            # Esta parte é opcional, dependendo do que você quer fazer se 'Studio Gravações' for selecionado
            if gravador_selecionado == 'Studio Gravações':
                # Seleção do Responsável e Data de Início
                nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
                responsavel_selecionado = st.selectbox('Selecione o Responsável:', nome_colaboradores)
            # Atualização de datas
            else:
                responsavel_selecionado = gravador_selecionado
            tipo_gravacao = st.selectbox('Selecione o tipo de gravação:', ['Silk', 'Tampografia', 'Sublimação','Laser','Bordado','DTF','DTF UV','Resina','Transfer','Especial'])
            data_gravacao = st.date_input('Data de Início:', value=today, max_value=today, format= 'DD/MM/YYYY')

        elif new_status == 'Gravação Finalizada':
            # Atualização de datas
            valor_gravacao = st.number_input('Digite o custo de gravação:', min_value= 0.00)
            data_gravacao = st.date_input('Data de Finalização:', value=today, max_value=today, format= 'DD/MM/YYYY')
            prox_etapa = st.selectbox('Selecione a próxima etapa:', ['Manuseio', 'Estoque'])

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        gravacao_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key =1)
        colaboradores_id = df_colaboradores['IDColaborador'].unique()

        # Botão para salvar as atualizações
        if st.button('Salvar', key =3):
            if int(gravacao_id) in colaboradores_id:
                gravacao_id_int = int(gravacao_id)
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]
                if new_status == 'Gravação Iniciada':
                    df_propostas.at[index, 'GravacaoTipo'] = tipo_gravacao
                    df_propostas.at[index, 'GravacaoStatus'] = new_status
                    df_propostas.at[index, 'GravacaoResponsavel'] = responsavel_selecionado
                    df_propostas.at[index, 'GravacaoDataInicio'] = pd.to_datetime(data_gravacao)
                    df_propostas.at[index, 'GravacaoIDInicio'] = gravacao_id_int
                    df_propostas.at[index, 'Gravador'] = gravador_selecionado
                else:          
                    df_propostas.at[index, 'GravacaoCusto'] = valor_gravacao
                    df_propostas.at[index, 'GravacaoStatus'] = new_status
                    df_propostas.at[index, 'Locale'] = prox_etapa
                    df_propostas.at[index, 'GravacaoDataFinal'] = pd.to_datetime(data_gravacao)
                    df_propostas.at[index, 'GravacaoIDFinal'] = gravacao_id_int
                df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
                st.success('Informações salvas com sucesso!')
                gravacao_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='', type='password', key =2)
            else:
                st.error('ID inválido!')