import streamlit as st
import time

# --- Configuração e CSS ---
st.set_page_config(layout="wide", page_title="Monitor de Chamada")

# --- Inicialização de Estado de Segurança ---
# Garante que as chaves existam antes de serem usadas.
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- CSS Personalizado para a Tela do Monitor ---
st.markdown("""
    <style>
    .big-font-senha {
        font-size: 150px !important;
        font-weight: 900;
        color: #e74c3c; /* Vermelho */
        text-align: center;
        padding-top: 20px;
    }
    .big-font-vaga {
        font-size: 100px !important;
        font-weight: 900;
        color: #3498db; /* Azul */
        text-align: center;
        padding-top: 20px;
    }
    .monitor-box {
        padding: 40px;
        margin: 20px 0;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        text-align: center;
        height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    /* Esconde a barra lateral e o menu de opções para o público */
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
## --- 🖥️ Tela do Monitor (Visão do Cliente) ---
# ==========================================================
    
st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

col_senha, col_vaga = st.columns(2)

with col_senha:
    st.markdown('<div class="monitor-box" style="background-color: #ffe0e0;"><h3>SENHA CHAMADA</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font-senha">{st.session_state.ultima_chamada_display}</p>', unsafe_allow_html=True)

with col_vaga:
    st.markdown('<div class="monitor-box" style="background-color: #e0f2ff;"><h3>DIRIJA-SE AO GUICHÊ</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font-vaga">{st.session_state.vaga_atual}</p>', unsafe_allow_html=True)

# Força a atualização da página a cada 1 segundo (Polling)
time.sleep(1) 
st.experimental_rerun()
