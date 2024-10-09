import streamlit as st
from pageProducao import recebimento, cq, estoque, gravacao, manuseio, expedicao, dashboard, cadastro_gravadores, cadastro_transportadoras, reposicoes, loteamento
from pageCompras import add_product, view_product, cadastro_clientes, cadastro_vendedores, cadastro_fornecedores, editar_opcoes


codigo = st.sidebar.text_input("Digite a senha para entrar no seu ambiente:")


# Verificação do código inserido e execução do script correspondente
if codigo:
    if codigo == '7H5UpKGnQ3':
        # Menu lateral para navegação
        st.sidebar.title("Navegação")
        page = st.sidebar.radio("Escolha uma Página", ['Dashboard','Recebimento', 'Controle de Qualidade', 'Estoque', 'Gravação', 'Manuseio','Expedição', 'Loteamento','Reposições','Cadastro Gravadores', 'Cadastro Transporadoras'])

        # Navegação entre páginas
        if page == 'Dashboard':
            dashboard.app()
        if page == 'Recebimento':
            recebimento.app()
        if page =='Controle de Qualidade':
            cq.app()
        if page == 'Estoque':
            estoque.app()
        if page == 'Gravação':
            gravacao.app()
        if page == 'Manuseio':
            manuseio.app()
        if page == 'Expedição':
            expedicao.app()
        if page == 'Reposições':
            reposicoes.app()
        if page =='Loteamento':
            loteamento.app()
        if page == 'Cadastro Gravadores':
            cadastro_gravadores.app()
        if page == 'Cadastro Transporadoras':
            cadastro_transportadoras.app()
    if codigo == '7ukuENT7Mv':
        # Menu lateral para navegação
        st.sidebar.title("Navegação")
        page = st.sidebar.radio("Escolha uma Página", ['Adicionar Propostas','Ver Produtos', 'Cadastro Clientes', 'Cadastro Vendedores', 'Cadastro Fornecedores', 'Editar Opções'])

        # Navegação entre páginas
        if page == 'Adicionar Propostas':
            add_product.app()
        if page == 'Ver Produtos':
            view_product.app()
        if page =='Cadastro Clientes':
            cadastro_clientes.app()
        if page == 'Cadastro Vendedores':
            cadastro_vendedores.app()
        if page == 'Cadastro Fornecedores':
            cadastro_fornecedores.app()
        if page == 'Editar Opções':
            editar_opcoes.app()