import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# --- Inicialização Global do Estado ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

st.title("Sistema de Chamada de Guichê 🚀")
st.markdown("---")

st.header("Instruções de Acesso Direto")
st.info("Devido a restrições de segurança do ambiente, a navegação deve ser feita por URL.")

base_url = st.get_option('server.baseUrlPath') # Obtém a URL base (ex: /guicheshopee)

st.markdown(f"""
### 🎛️ Para o Atendente (Controle)
**Use esta URL:** `https://play.google.com/store/apps/details?id=com.flaviodesign.doit&hl=pt/Atendente`
<a href="{base_url}/Atendente" target="_self"><button style="background-color: #2ecc71; color: white; padding: 10px 20px; border-radius: 5px; border: none; font-size: 16px; cursor: pointer;">CLIQUE PARA ABRIR O ATENDENTE</button></a>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"""
### 🖥️ Para o Monitor (Tela Pública)
**Use esta URL:** `https://play.google.com/store/apps/details?id=com.flaviodesign.doit&hl=pt/Monitor`
<a href="{base_url}/Monitor" target="_blank"><button style="background-color: #3498db; color: white; padding: 10px 20px; border-radius: 5px; border: none; font-size: 16px; cursor: pointer;">CLIQUE PARA ABRIR O MONITOR</button></a>
""", unsafe_allow_html=True)

st.caption("Abra a URL do Monitor em uma tela separada para o público.")
