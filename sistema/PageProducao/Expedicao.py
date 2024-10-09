import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    data_transportadoras = pd.read_excel('OpcoesTransportadoras.xlsx')
    # Preparando os dados conforme necessário
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'ExpedicaoID' in data_propostas.columns:
        data_propostas['ExpedicaoID'] = pd.to_datetime(data_propostas['ExpedicaoID'], errors='coerce')
    return data_propostas, data_colaboradores, data_transportadoras

def app():
    df_propostas, df_colaboradores, df_transportadoras = load_data()

    # Normalizando a coluna 'Locale'
    df_propostas['Locale'] = df_propostas['Locale'].str.strip()

    # Filtrando com a versão normalizada de 'expedição'
    df_expedicao = df_propostas[df_propostas['Locale'] == 'Expedição'].copy()

    st.title('Gerenciamento de Expedição')
    
    if len(df_expedicao) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:
        st.subheader("Produtos para Manuseio")
        df_expedicao['NumeroProposta'] = df_expedicao['NumeroProposta'].astype(str)
        df_expedicao['DataEntrega'] = pd.to_datetime(df_expedicao['DataEntrega'], errors='coerce')
        df_expedicao['DataEntrega'] = df_expedicao['DataEntrega'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_expedicao[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_expedicao['Codigo_Proposta_Lote'].unique())

        tipo_entrega = st.selectbox('Selecione o tipo de Entrega:', ['CIF','FOB'])

        if tipo_entrega == 'CIF':
            nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
            responsavel_selecionado = st.selectbox('Selecione o Entregador:', nome_colaboradores)
        else:
            nome_colaboradores = df_transportadoras['NomeTransportadora'].unique()
            responsavel_selecionado = st.selectbox('Selecione a Transportadora:', nome_colaboradores)

        data_expedicao = st.date_input('Data de Saída:', value=today, max_value=today, format= 'DD/MM/YYYY')
        hora_expedicao = st.time_input('Hora de Saída:')
        cod_rastreio = st.text_input('Codigo de rastreio ou nota:')

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        manuseio_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key =1)
        colaboradores_id = df_colaboradores['IDColaborador'].unique()

        # Botão para salvar as atualizações
        if st.button('Salvar', key =3):
            if int(manuseio_id) in colaboradores_id:
                manuseio_id_int = int(manuseio_id)
                index = df_propostas[df_propostas['Codigo_Proposta_Lote'] == produto_selecionado].index[0]

                df_propostas.at[index, 'Entregador'] = responsavel_selecionado
                df_propostas.at[index, 'TipoEntrega'] = tipo_entrega
                df_propostas.at[index, 'DataDeSaida'] = pd.to_datetime(data_expedicao)
                df_propostas.at[index, 'HoraDeSaida'] = hora_expedicao
                df_propostas.at[index, 'Locale'] = 'Saiu para entrega'
                df_propostas.at[index, 'ExpedicaoID'] = manuseio_id_int
                df_propostas.at[index, 'Rastreio'] = cod_rastreio

                df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição
                st.success('Informações salvas com sucesso!')
                manuseio_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value='', type='password', key =2)
            else:
                st.error('ID inválido!')