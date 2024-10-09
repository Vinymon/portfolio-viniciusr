import streamlit as st
import pandas as pd

def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns and 'NumeroProposta' in data_propostas.columns:
        data_propostas['Codigo_Proposta_Lote'] = (
            data_propostas['Codigo'].astype(str) + " - " +
            data_propostas['NumeroProposta'].astype(str) + " - " +
            data_propostas['Lote'].astype(str)
        )
    if 'QuantidadeCaixa' not in data_propostas.columns:
        data_propostas['QuantidadeCaixa'] = 0
    return data_propostas



def app():
    st.title('Solicitação de NF')
    if 'caixas' not in st.session_state:
        st.session_state.caixas = []
    df_propostas = load_data()
    df_nf = df_propostas[df_propostas['Locale'] == 'Solicitação NF'].copy()

    if df_nf.empty:
        st.write('Não possuem produtos nesta etapa.')
    else:
        st.subheader("Produtos para solicitação de NF")
        df_nf['NumeroProposta'] = df_nf['NumeroProposta'].astype(str)
        df_nf['Quantidade'] = df_nf['Quantidade'].astype(int)
        df_nf['QuantidadeSobra'] = df_nf['QuantidadeSobra'].astype(int)
        df_nf['DataEntrega'] = pd.to_datetime(df_nf['DataEntrega'], errors='coerce')
        df_nf['DataEntrega'] = df_nf['DataEntrega'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_nf[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)
        st.write("---")

        # Botão para adicionar uma nova caixa
        if st.button("Adicionar Caixa"):
            st.session_state.caixas.append({'produtos': [], 'altura': None, 'largura': None, 'profundidade': None, 'peso': None})

        for i, caixa in enumerate(st.session_state.caixas):
            with st.expander(f"Caixa {i + 1}"):
                caixa['altura'] = st.number_input("Altura", key=f'altura_{i}')
                caixa['largura'] = st.number_input("Largura", key=f'largura_{i}')
                caixa['profundidade'] = st.number_input("Profundidade", key=f'profundidade_{i}')
                caixa['peso'] = st.number_input("Peso", key=f'peso_{i}')
                
                produto_selecionado = st.selectbox("Selecione um Produto", df_nf['Codigo_Proposta_Lote'].unique(), key=f'produto_{i}')
                quantidade = st.number_input("Quantidade", min_value=1, value=1, key=f'quantidade_{i}')

                # Botão para adicionar produto à caixa
                if st.button("Adicionar Produto", key=f'add_{i}'):
                    nome_produto = df_nf[df_nf['Codigo_Proposta_Lote'] == produto_selecionado].iloc[0]['Nome']
                    caixa['produtos'].append({
                        'produto': produto_selecionado,
                        'quantidade': quantidade,
                        'nome': nome_produto
                    })

                # Lista os produtos na caixa com a opção de remover
                for j, prod in enumerate(caixa['produtos']):
                    st.write(f"Produto: {prod['nome']}, Quantidade: {prod['quantidade']}")
                    if st.button(f"Remover Produto {j + 1}", key=f'remove_{i}_{j}'):
                        caixa['produtos'].pop(j)

    def salvar_informacoes():
        df_propostas = load_data()
        
        # Preparar as informações das caixas para salvar
        caixas_info = []
        for i, caixa in enumerate(st.session_state.caixas):
            for prod in caixa['produtos']:
                # Encontrar as informações detalhadas do produto usando 'Codigo_Proposta_Lote'
                produto_info = df_propostas[df_propostas['Codigo_Proposta_Lote'] == prod['produto']].iloc[0]
                # Atualizar 'Locale' no DataFrame original para "Expedição"
                df_propostas.loc[df_propostas['Codigo_Proposta_Lote'] == prod['produto'], 'Locale'] = 'Expedição'
                # Adicionar informações da caixa e do produto a serem salvas
                caixas_info.append({
                    'Caixa': str(produto_info['NumeroProposta']) + ' - ' + str(i + 1),
                    'Nome': produto_info['Nome'],
                    'Codigo': produto_info['Codigo'],
                    'NumeroProposta': produto_info['NumeroProposta'],
                    'QuantidadeCaixa': prod['quantidade'],
                    'Altura': caixa['altura'],
                    'Largura': caixa['largura'],
                    'Profundidade': caixa['profundidade'],
                    'Peso': caixa['peso'],
                    'Status': 'Pendente'
                })

        # Criar DataFrame com as informações das caixas
        df_caixas_info = pd.DataFrame(caixas_info)
        
        # Salvar informações das caixas no arquivo 'Caixas_Info.xlsx'
        df_caixas_info.to_excel('Caixas_Info.xlsx', index=False)
        
        # Salvar o DataFrame atualizado das propostas em 'Propostas_Atualizadas.xlsx'
        df_propostas.to_excel('Propostas.xlsx', index=False)
        
        st.success('Informações das caixas salvas.')


    # Inclusão do botão para chamar salvar_informacoes() e o restante da implementação do app()
    if st.button("Salvar Caixas e Atualizar Propostas"):
        salvar_informacoes()