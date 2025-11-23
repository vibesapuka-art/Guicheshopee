import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# ATENÇÃO: SUBSTITUA ESTA VARIÁVEL PELA URL ATIVA ATUAL DO SEU APLICATIVO!
# Exemplo (NÃO COPIE): APP_URL_BASE = "https://guicheshopee-h...streamli.app"
APP_URL_BASE = "COLOQUE_AQUI_A_URL_COMPLETA_DO_SEU_APP" 

# CSS para esconder a barra lateral e o menu de opções em todas as visualizações
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
    }
    /* Estilos para botões na Home Page */
    .link-button-style {
        text-decoration: none;
        display: block;
        width: 100%;
        text-align: center;
        padding: 15px 10px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        margin: 15px 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# --- Inicialização Global do Estado ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- Layout da Home Page ---
st.title("Sistema de Guichê: Escolha seu Modo")
st.markdown("---")
st.header("Qual é a sua função nesta tela?")

# --- Botão Atendente (Link Absoluto) ---
st.markdown(
    f"""
    ### 🎛️ Para o Atendente (Controle)
    <a href="{APP_URL_BASE}/Atendente" target="_self" class="link-button-style" style="background-color: #2ecc71; color: white;">
        CLIQUE PARA ABRIR O ATENDENTE
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Botão Monitor (Link Absoluto - Nova Aba) ---
st.markdown(
    f"""
    ### 🖥️ Para o Monitor (Tela Pública)
    <a href="{APP_URL_BASE}/Monitor" target="_blank" class="link-button-style" style="background-color: #3498db; color: white;">
        CLIQUE PARA ABRIR O MONITOR
    </a>
    """,
    unsafe_allow_html=True
)

st.caption("O Monitor abrirá em uma nova aba. O Atendente abrirá nesta aba. Se o problema de 'ir e voltar' persistir, a única solução será usar a barra lateral ou mudar o domínio de hospedagem.")
