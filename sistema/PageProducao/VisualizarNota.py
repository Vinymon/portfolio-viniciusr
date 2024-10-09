import streamlit as st
import pandas as pd
import fitz
import os

diretorio_upload = "./ArquivosNF"

# Função única para carregar os dados
def load_data():
    data_propostas = pd.read_excel('Propostas.xlsx')
    # Preparando os dados conforme necessário
    if 'Codigo' in data_propostas.columns and 'Lote' in data_propostas.columns:
        data_propostas['Codigo_Lote'] = data_propostas['Codigo'].astype(str) + " - " + data_propostas['Lote'].astype(str)
    return data_propostas

def app():

    df_propostas = load_data()
    
    # Filtrando propostas com OPStatus 'OP Pendente'
    df_manuseio = df_propostas.loc[(df_propostas['NotaStatus'] == 'Emitido') &
                               (~df_propostas['Locale'].isin(['', 'Entregue']))].copy()
    
    # Convertendo 'DataEntrega' para o formato de data corretamente e depois para string, para evitar problemas de conversão posteriormente
    df_manuseio['DataEntrega'] = pd.to_datetime(df_manuseio['DataEntrega'], errors='coerce').dt.strftime('%d/%m/%Y')
    
    # Agrupando por 'NumeroProposta' e mantendo o primeiro valor encontrado para as outras colunas relevantes
    df_agrupado = df_manuseio.groupby('NumeroProposta', as_index=False).first()
    
    contagem_locale = df_agrupado.shape[0]

    st.title('Gerenciamento de NF')
    
    # Exibindo a contagem de OPs pendentes
    st.subheader(f"Quantidade de notas emitidas: {contagem_locale}")
    st.write('---')

    st.subheader("NF's emitidas")
    df_agrupado['NumeroProposta'] = df_agrupado['NumeroProposta'].astype(str)
    # Exibindo apenas as colunas especificadas
    st.dataframe(df_agrupado[['Locale','Vendedor', 'Cliente', 'DataEntrega', 'NumeroProposta', 'NotaStatus']], use_container_width=True)
    st.write("---")

    # Permitindo ao usuário selecionar um produto para alterar o status para 'OP Impressa'
    st.subheader("Selecione uma proposta para visualizar a NF")
    # Lista de arquivos para seleção
    if os.path.exists(diretorio_upload):
        files = [f for f in os.listdir(diretorio_upload) if os.path.isfile(os.path.join(diretorio_upload, f))]
        selected_file = st.selectbox("Escolha um arquivo para visualizar", files)
        
        # Visualização do PDF selecionado
        if selected_file:
            file_path = os.path.join(diretorio_upload, selected_file)
            with fitz.open(file_path) as pdf:
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)  # Carregar a página
                    pix = page.get_pixmap()  # Renderizar página como um pixmap (imagem)
                    img = pix.tobytes("png")  # Converter o pixmap em bytes PNG
                    st.image(img, caption=f"Página {page_num + 1}", use_column_width=True)

            # Botão de download
            with open(file_path, "rb") as file:
                btn = st.download_button(
                    label="Baixar PDF",
                    data=file,
                    file_name=selected_file,
                    mime="application/pdf"
                )