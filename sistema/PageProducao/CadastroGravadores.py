import streamlit as st
import pandas as pd

def salvar_dados(nome, telefone, endereco):

    new_data = pd.DataFrame({'NomeGravador': [nome], 'TelefoneGravador': [telefone], 'EnderecoGravador': [endereco]})

    try:
        df = pd.read_excel('OpcoesGravadores.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['NomeGravador', 'TelefoneGravador', 'EnderecoGravador'])

    df = pd.concat([df, new_data], ignore_index=True)

    df.to_excel('OpcoesGravadores.xlsx', index=False)

def load_full_data(filename):
    return pd.read_excel(filename)

def app():

    st.title("Cadastro de Informações")

    nome = st.text_input("Nome do Gravador")
    telefone = st.text_input("Telefone do Gravador")
    endereco = st.text_input("Endereço do Gravador")

    df_colaboradores = load_full_data('OpcoesStudioGravacoes.xlsx')
    id_colaboradores = df_colaboradores['IDColaborador'].unique()

    placeholder = st.empty()
    cadastro_id = placeholder.text_input("Digite seu ID para confirmar a atualização:",type='password',key=1)
    
    if st.button("Salvar", key=3):
        if int(cadastro_id) in id_colaboradores:
            salvar_dados(nome, telefone, endereco)
            st.success('Dados atualizados com sucesso!')
            cadastro_id = placeholder.text_input('Digite seu ID para confirmar a atualização', value='', key=2, type='password')
        else:
            st.error('ID inválido.')