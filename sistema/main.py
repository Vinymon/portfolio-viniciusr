import streamlit as st
from PageCompras import Atrasos, CadastroPropostas, VerProdutos, CadastroClientes, CadastroVendedores, CadastroFornecedores, EditarOpcoes, VisibilidadeCompras
from PageProducao import CadastroGravadores, CadastroTransportadoras, Cq, Dashboard, Estoque, Expedicao, Gravacao, Loteamento, Manuseio, Recebimento, Reposicoes, VisualizarOP, VisualizarNota, VisibilidadeGeral, SolicitacaoNF
from PageADM import InfoNota, PgHoraStudio
from PageLayout import InfoLayout, BaixaEntrega, Gastos, HoraExtra
from PageClaudio import DashboardClaudio
from PageRelatorio import dashboardvendas
from PageVendedores import Arlete, MarcosVinicius, Wellington, Juliane, Naldo, Rodolfo

st.set_page_config(page_title='ConnectERP', page_icon= '🛠',layout = 'wide')

st.sidebar.image("LogoConnect.png", use_column_width=True)
codigo = st.sidebar.text_input("Digite a senha para entrar no seu ambiente:")

if codigo == '73blkfgjn':
    Rodolfo.app()

if codigo == '40q08hm2b':
    Naldo.app()

if codigo == '65u7d78lv':
    Juliane.app()

if codigo == '8uwljil5r':
    Wellington.app()

if codigo == '3zhd5cyj':
    Arlete.app()

if codigo == '017i4v9xj':
    MarcosVinicius.app()

if codigo == 'relatorio':
    dashboardvendas.app()

if codigo == '1987':
    page = st.sidebar.radio("Escolha uma Página", ['Solicitações de OP','Confirmação Entrega'])
    if page == 'Solicitações de OP':
        InfoLayout.app()
    if page == 'Confirmação Entrega':
        BaixaEntrega.app()

if codigo == '484950':
    InfoNota.app()

if codigo == '7H5UpKGnQ3':
    page = st.sidebar.radio("Escolha uma Página", ['Atrasos','Adicionar Propostas','Ver Produtos', 'Cadastro Clientes', 'Cadastro Vendedores', 'Cadastro Fornecedores', 'Editar Opções', 'Visibilidade Geral'])
    # Navegação entre páginas
    if page == 'Atrasos':
        Atrasos.app()
    if page == 'Adicionar Propostas':
        CadastroPropostas.app()
    if page == 'Ver Produtos':
        VerProdutos.app()
    if page =='Cadastro Clientes':
        CadastroClientes.app()
    if page == 'Cadastro Vendedores':
        CadastroVendedores.app()
    if page == 'Cadastro Fornecedores':
        CadastroFornecedores.app()
    if page == 'Editar Opções':
        EditarOpcoes.app()
    if page == 'Visibilidade Geral':
        VisibilidadeCompras.app()

if codigo == '7ukuENT7Mv':
    page = st.sidebar.radio("Escolha uma Página", ['Dashboard','Recebimento', 'Controle de Qualidade', 'Gravação', 'Manuseio','Solicitação NF','Expedição', 'Estoque', 'Loteamento','Reposições','Cadastro Gravadores', 'Cadastro Transporadoras', 'Visualizar OPs', 'Visualizar NF','Visibilidade Geral'])
    # Navegação entre páginas
    if page == 'Dashboard':
        Dashboard.app()
    if page == 'Recebimento':
        Recebimento.app()
    if page == 'Controle de Qualidade':
        Cq.app()
    if page == 'Gravação':
        Gravacao.app()
    if page == 'Manuseio':
        Manuseio.app()
    if page =='Solicitação NF':
        SolicitacaoNF.app()
    if page == 'Expedição':
        Expedicao.app()
    if page == 'Estoque':
        Estoque.app()
    if page == 'Reposições':
        Reposicoes.app()
    if page == 'Loteamento':
        Loteamento.app()
    if page == 'Cadastro Gravadores':
        CadastroGravadores.app()
    if page == 'Cadastro Transporadoras':
        CadastroTransportadoras.app()
    if page == 'Visualizar OPs':
        VisualizarOP.app()
    if page == 'Visualizar NF':
        VisualizarNota.app()
    if page == 'Visibilidade Geral':
        VisibilidadeGeral.app()

if codigo == 'claudio':
    page = st.sidebar.selectbox("Escolha uma área", ['Compras','Adm', 'Arte Finalista', 'Produção'])
    st.sidebar.write('---')
    if page == 'Compras':
        page = st.sidebar.selectbox("Escolha uma Página", ['Atrasos','Adicionar Propostas','Ver Produtos', 'Cadastro Clientes', 'Cadastro Vendedores', 'Cadastro Fornecedores', 'Editar Opções','Visibilidade Geral'])
        if page == 'Atrasos':
            Atrasos.app()
        if page == 'Adicionar Propostas':
            CadastroPropostas.app()
        if page == 'Ver Produtos':
            VerProdutos.app()
        if page =='Cadastro Clientes':
            CadastroClientes.app()
        if page == 'Cadastro Vendedores':
            CadastroVendedores.app()
        if page == 'Cadastro Fornecedores':
            CadastroFornecedores.app()
        if page == 'Editar Opções':
            EditarOpcoes.app()
        if page == 'Visibilidade Geral':
            VisibilidadeCompras.app()

    if page == 'Adm':
        page = st.sidebar.selectbox("Escolha uma Página", ['Solicitação NF', 'Planilha Horas Extras'])
        if page == 'Solicitação NF':
            InfoNota.app()
        if page == 'Planilha Horas Extras':
            PgHoraStudio.app()
        

    if page == 'Arte Finalista':
        page = st.sidebar.selectbox("Escolha uma Página", ['Solicitações de OP','Confirmação Entrega','Cadastro de Gastos','Hora Extra'])
        if page == 'Solicitações de OP':
            InfoLayout.app()
        if page == 'Confirmação Entrega':
            BaixaEntrega.app()
        if page == 'Cadastro de Gastos':
            Gastos.app()
        if page == 'Hora Extra':
            HoraExtra.app()

    if page == 'Produção':
        page = st.sidebar.selectbox("Escolha uma Página", ['Dashboard','Recebimento', 'Controle de Qualidade', 'Gravação', 'Manuseio','Solicitação NF','Expedição', 'Estoque', 'Loteamento','Reposições','Cadastro Gravadores', 'Cadastro Transporadoras', 'Visualizar OPs', 'Visualizar NF','Visibilidade Geral'])
        if page == 'Dashboard':
            Dashboard.app()
        if page == 'Recebimento':
            Recebimento.app()
        if page == 'Controle de Qualidade':
            Cq.app()
        if page == 'Gravação':
            Gravacao.app()
        if page == 'Manuseio':
            Manuseio.app()
        if page =='Solicitação NF':
            SolicitacaoNF.app()
        if page == 'Expedição':
            Expedicao.app()
        if page == 'Estoque':
            Estoque.app()
        if page == 'Reposições':
            Reposicoes.app()
        if page == 'Loteamento':
            Loteamento.app()
        if page == 'Cadastro Gravadores':
            CadastroGravadores.app()
        if page == 'Cadastro Transporadoras':
            CadastroTransportadoras.app()
        if page == 'Visualizar OPs':
            VisualizarOP.app()
        if page == 'Visualizar NF':
            VisualizarNota.app()
        if page == 'Visibilidade Geral':
            VisibilidadeGeral.app()

