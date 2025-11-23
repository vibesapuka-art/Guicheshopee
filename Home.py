import streamlit as st

# --- Configuração e Inicialização do Estado ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# Inicializa o gatilho de navegação
if 'navigate_to' not in st.session_state:
    st.session_state.navigate_to = None

# Inicialização Global do Estado do Guichê (Se não existir, cria)
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# CSS para esconder a barra lateral e o menu
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
    }
    .monitor-box-home {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Lógica de Navegação Controlada ---

# Se o gatilho foi ativado (após o clique do botão), navegue e finalize a execução
if st.session_state.navigate_to == "monitor":
    st.session_state.navigate_to = None # Limpa o gatilho
    st.switch_page("pages/1_Monitor")
elif st.session_state.navigate_to == "atendente":
    st.session_state.navigate_to = None # Limpa o gatilho
    st.switch_page("pages/2_Atendente")


# --- Layout da Home Page ---
st.title("Sistema de Guichê: Escolha seu Modo")
st.markdown("---")
st.header("Qual é a sua função nesta tela?")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="monitor-box-home" style="background-color: #e0f2ff;"><h3>TELA DO CLIENTE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 Ação: Ao clicar, ATIVA o gatilho
    if st.button("Sou MONITOR", key="btn_monitor", type="primary"):
        st.session_state.navigate_to = "monitor"
        # Reroda o script para que a lógica de navegação acima seja executada
        st.rerun() 

with col2:
    st.markdown('<div class="monitor-box-home" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 Ação: Ao clicar, ATIVA o gatilho
    if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
        st.session_state.navigate_to = "atendente"
        # Reroda o script para que a lógica de navegação acima seja executada
        st.rerun() 
        
st.markdown("---")
st.caption("Acesse a mesma URL em telas diferentes para sincronizar. Você só precisa clicar no botão uma vez por tela.")
