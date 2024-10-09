import streamlit as st
import pandas as pd

FILE_PATH = "Propostas.xlsx"

def unificar_produtos(df, produto1, produto2):
    # Encontrar os índices dos produtos selecionados
    idx1 = df.index[df['Codigo_Lote'] == produto1][0]
    idx2 = df.index[df['Codigo_Lote'] == produto2][0]

    # Verificando se os produtos têm o mesmo 'Locale'
    if df.at[idx1, 'Locale'] != df.at[idx2, 'Locale']:
        return df, False, "Os produtos devem ter o mesmo 'Locale' para serem unificados."

    # Somar as quantidades
    nova_quantidade = df.at[idx1, 'Quantidade'] + df.at[idx2, 'Quantidade']

    # Atualizar a linha do primeiro produto
    df.at[idx1, 'Quantidade'] = nova_quantidade
    # O 'Lote' é mantido como o do primeiro produto

    # Remover a linha do segundo produto
    df = df.drop(idx2)

    return df, True, ""

# Função para ler os dados
def load_data():
    df = pd.read_excel(FILE_PATH)
    # Criando uma nova coluna que combina 'Codigo', 'Nome' e 'NumeroProposta'
    df['Codigo_Nome_Proposta'] = df['Codigo'].astype(str) + ' - ' + df['Nome'].astype(str) + ' - ' + df['NumeroProposta'].astype(str)
    # Criando uma nova coluna que combina 'Codigo' e 'Lote'
    df['Codigo_Lote'] = df['Codigo'].astype(str) + ' - ' + df['NumeroProposta'].astype(str) + ' - ' + df['Lote'].astype(str)
    return df

# Função para verificar a existência de um lote duplicado
def is_duplicate_lote(df, codigo, num_proposta, lote):
    return ((df['Codigo'] == codigo) & 
            (df['NumeroProposta'] == num_proposta) & 
            (df['Lote'] == f"Lote {lote}")).any()

# Função para atualizar a linha existente e adicionar uma nova linha
def update_and_add_rows(df, selected_product, updated_qty, original_lote, new_qty, new_lote):
    row_index = df[df['Codigo_Lote'] == selected_product].index[0]
    original_qty = df.at[row_index, 'Quantidade']
    codigo = df.at[row_index, 'Codigo']
    num_proposta = df.at[row_index, 'NumeroProposta']

    # Verificando se a soma das novas quantidades é igual à quantidade original
    if updated_qty + new_qty != original_qty:
        return df, False, "A soma das quantidades não corresponde à quantidade original do produto."

    # Verificando se o novo lote está duplicado
    if is_duplicate_lote(df, codigo, num_proposta, new_lote):
        return df, False, "Não é possível ter lotes duplicados para o mesmo código e número de proposta."

    # Atualizando a linha existente e criando uma nova linha
    df.at[row_index, 'Quantidade'] = updated_qty

    new_row = df.loc[row_index].copy()
    new_row['Quantidade'] = new_qty
    new_row['Lote'] = f"Lote {new_lote}"
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df, True, ""

# Função para salvar as alterações de volta no arquivo Excel
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Página principal do Streamlit
def app():
    st.title("Separador de Produtos")

    df = load_data()

    # Filtrar produtos com 'Locale' diferente de 'Estoque' e 'Coletado'
    produtos_filtrados = df[~df['Locale'].isin(['Estoque', 'Coletado', 'Saiu para entrega']) & df['Locale'].notna() & (df['Locale'] != '')]

    if len(produtos_filtrados) ==0:
        st.write('Não existem produtos disponíveis para loteamento')
    else:
        # Dropdown para seleção do produto baseado em 'Codigo' - 'Nome' - 'NumeroProposta'
        produto_list = produtos_filtrados['Codigo_Nome_Proposta'].unique()
        selected_codigo_nome_proposta = st.selectbox("Selecione um Produto (Código - Nome - Proposta)", produto_list)


        # Exibir DataFrame com todos os lotes do produto selecionado
        if selected_codigo_nome_proposta:
            selected_codigo = selected_codigo_nome_proposta.split(' - ')[0]
            df_produto_selecionado = df[df['Codigo'] == selected_codigo]

            # Mostrando os dados em uma tabela para o produto selecionado
            df_produto_selecionado['Quantidade'] = df_produto_selecionado['Quantidade'].astype(int)
            df_produto_selecionado['QuantidadeSobra'] = df_produto_selecionado['QuantidadeSobra'].astype(int)
            df_produto_selecionado['NumeroProposta'] = df_produto_selecionado['NumeroProposta'].astype(str)
            df_produto_selecionado['DataEntrega'] = pd.to_datetime(df_produto_selecionado['DataEntrega'], errors='coerce')
            df_produto_selecionado['DataEntrega'] = df_produto_selecionado['DataEntrega'].dt.strftime('%d/%m/%Y')
            st.dataframe(df_produto_selecionado[['Nome', 'Codigo', 'Vendedor', 'Cliente','GravacaoResponsavel', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'OPStatus','Locale','Tipo','Lote','DataEntrega','LocalEntrega']], use_container_width=True)

            # Dropdown para seleção do lote baseado em 'Codigo_Lote' para o produto selecionado
            lote_list = df_produto_selecionado['Codigo_Lote'].unique()
            selected_product = st.selectbox("Selecione um Lote (Código - Proposta - Lote)", lote_list)

            st.write('---')

            # Encontrando o lote atual do produto selecionado
            current_lote = df[df['Codigo_Lote'] == selected_product]['Lote'].iloc[0]

            # Campos editáveis para atualizar a linha existente e adicionar uma nova linha
            st.subheader("Atualizar e Adicionar Produto")
            updated_qty = st.number_input("Atualizar Quantidade do " + str(current_lote) , value=0, key='updated_qty')


            st.write('---')
            new_qty = st.number_input("Nova Quantidade", value=0, key='new_qty')
            new_lote = st.number_input("Número do Novo Lote", value=0, key='new_lote', format='%d')

            # Botão para salvar
            if st.button("Salvar Alterações"):
                df, valid_operation, message = update_and_add_rows(df, selected_product, updated_qty, current_lote, new_qty, new_lote)
                if valid_operation:
                    save_data(df)
                    st.success("Alterações Salvas com Sucesso!")
                else:
                    st.error(message)
    st.write('---')
    st.subheader("Produtos possíveis de unificar")

    # Agrupando os dados pelas colunas especificadas
    grupos = df.groupby(['Locale', 'Codigo', 'Nome', 'DataEntrega'])

    # Filtrando os grupos que têm mais de uma linha
    produtos_similares = pd.DataFrame()
    for _, grupo in grupos:
        if len(grupo) > 1:
            produtos_similares = pd.concat([produtos_similares, grupo])

    # Exibindo os produtos similares, se houver
    if not produtos_similares.empty:
        
        produtos_similares['Quantidade'] = produtos_similares['Quantidade'].astype(int)
        produtos_similares['QuantidadeSobra'] = produtos_similares['QuantidadeSobra'].astype(int)
        produtos_similares['NumeroProposta'] = produtos_similares['NumeroProposta'].astype(str)
        produtos_similares['DataEntrega'] = pd.to_datetime(produtos_similares['DataEntrega'], errors='coerce')
        produtos_similares['DataEntrega'] = produtos_similares['DataEntrega'].dt.strftime('%d/%m/%Y')
        st.dataframe(produtos_similares[['Nome', 'Codigo', 'Cliente','DataEntrega', 'Quantidade','QuantidadeSobra', 'NumeroProposta', 'GravacaoResponsavel', 'GravacaoTipo','Locale', 'NotaStatus', 'OPStatus','Tipo', 'Vendedor','Lote','LocalEntrega']], use_container_width=True)

        st.write('---')
        st.subheader("Unificar Produtos")

        # Lista de produtos na tabela de produtos similares
        lista_produtos_similares = produtos_similares['Codigo_Lote'].tolist()

        # Dropdowns para selecionar os produtos a serem unificados
        produto1 = st.selectbox("Selecione o primeiro produto para unificação:", lista_produtos_similares, key='produto1')
        produto2 = st.selectbox("Selecione o segundo produto para unificação:", lista_produtos_similares, key='produto2')

        # Botão para unificar os produtos
        if st.button("Unificar"):
            if produto1 != produto2:
                df, valid_operation, message = unificar_produtos(df, produto1, produto2)
                if valid_operation:
                    save_data(df)
                    st.success("Produtos unificados com sucesso!")
                else:
                    st.error(message)
            else:
                st.error("Selecione dois produtos diferentes para unificar.")