import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# CSS para esconder a barra lateral de navegação aqui
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
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

# --- Funções de Redirecionamento ---
# Não precisam de definição, pois a chamada direta já funciona
# Apenas a lógica do botão precisa ser corrigida

# --- Layout da Home Page ---
st.title("Sistema de Guichê: Escolha seu Modo")
st.markdown("---")
st.header("Qual é a sua função nesta tela?")

# CSS para os botões da Home Page
st.markdown("""
    <style>
    .monitor-box-home {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="monitor-box-home" style="background-color: #e0f2ff;"><h3>TELA DO CLIENTE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 CORREÇÃO: switch_page SÓ É CHAMADO SE O BOTÃO FOR CLICADO
    if st.button("Sou MONITOR", key="btn_monitor", type="primary"):
        st.switch_page("pages/1_Monitor") 

with col2:
    st.markdown('<div class="monitor-box-home" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 CORREÇÃO: switch_page SÓ É CHAMADO SE O BOTÃO FOR CLICADO
    if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
        st.switch_page("pages/2_Atendente") 
        
st.markdown("---")
st.caption("Acesse a mesma URL em telas diferentes para sincronizar. Você só precisa clicar no botão uma vez por tela.")
