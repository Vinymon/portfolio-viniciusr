import streamlit as st
import pandas as pd
from datetime import datetime

today = datetime.now().date()

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    data_colaboradores = pd.read_excel('OpcoesStudioGravacoes.xlsx')
    # Preparando os dados conforme necessário
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['NumeroProposta'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    if 'DataRecebimento' in data_propostas.columns:
        data_propostas['DataRecebimento'] = pd.to_datetime(data_propostas['DataRecebimento'], errors='coerce')
    return data_propostas, data_colaboradores

def app():
    df_propostas, df_colaboradores = load_data()
    
    # Filtrando vendedores com propostas em CQ
    df_cq = df_propostas[df_propostas['StatusMaterial'].isin(['Pronto', 'Atrasado'])]

    st.title('Gerenciamento de Recebimento')
    
    if len(df_cq) == 0:
        st.write('Não possuem produtos nesta etapa.')
    else:
        st.subheader("Produtos para recebimento")
        df_cq['DataRecebimento'] = pd.to_datetime(df_cq['DataRecebimento'], errors='coerce')
        df_cq['DataRecebimento'] = df_cq['DataRecebimento'].dt.strftime('%d/%m/%Y')
        df_cq['NumeroProposta'] = df_cq['NumeroProposta'].astype(str)
        st.dataframe(df_cq[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Seleção e manipulação do produto
        produto_selecionado = st.selectbox("Selecione um Produto ('Codigo' - 'Proposta' - 'Lote'):", df_cq['Codigo_Proposta_Lote'].unique())
        index = df_cq[df_cq['Codigo_Proposta_Lote'] == produto_selecionado].index[0]

        # Atualização do Status do Material
        new_status = st.radio("Atualizar Status do Material", ['Recebido', 'Atrasado'])

        # Seleção do Responsável e Data de Início
        nome_colaboradores = df_colaboradores['NomeColaborador'].unique()
        colaboradores_id = df_colaboradores['IDColaborador'].unique()
        responsavel_selecionado = st.selectbox('Selecione o Responsável:', nome_colaboradores)
        data_inicio = st.date_input('Data de Início:', value=today, max_value=today, format = 'DD/MM/YYYY')
        hora_recebimento = st.time_input("Hora de Recebimento")

        # Campo de ID com senha para confirmação
        placeholder = st.empty()
        recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", type='password', key=1)
        op_status = 'OP Pendente'

        # Botão para salvar as atualizações
        if st.button('Salvar', key =3):
            if int(recebimento_id) in colaboradores_id:
                df_propostas.at[index, 'DataRecebimento'] = pd.to_datetime(data_inicio)
                df_propostas.at[index, 'StatusMaterial'] = new_status
                df_propostas.at[index, 'HoraRecebimento'] = hora_recebimento.strftime('%H:%M')

                st.success('Informações salvas com sucesso!')
                recebimento_id = placeholder.text_input("Digite seu ID para confirmar a atualização:", value = '',type='password', key=2)
                if new_status == 'Recebido':
                    df_propostas.at[index, 'Locale'] = 'CQ'
                    df_propostas.at[index, 'IDRecebimento'] = recebimento_id
                    df_propostas.at[index, 'RecebimentoResponsavel'] = responsavel_selecionado
                    df_propostas.at[index, 'OPStatus'] = op_status
                else:
                    df_propostas.at[index, 'Locale'] = 'Recebimento'
                    df_propostas.at[index, 'IDRecebimento'] = recebimento_id
                df_propostas.to_excel('Propostas.xlsx', index=False)  # Salvando em novo arquivo para evitar sobreposição durante o teste
            else:
                st.error('ID inválido!')