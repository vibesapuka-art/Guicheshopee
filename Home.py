import streamlit as st

# Define o estado da barra lateral como expandida para facilitar o uso
st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="expanded") 

# --- Inicialização Global do Estado ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

st.title("👋 Sistema de Chamada de Guichê")
st.markdown("---")

st.header("Instruções de Acesso")

st.info("""
O seu sistema de guichê está funcionando na arquitetura de múltiplas páginas!
**A navegação é feita pela Barra Lateral à esquerda.**
""")

st.markdown("""
### 🎛️ Para o Atendente (Controle)
**Clique em '2 Atendente'** na Barra Lateral.
""")

st.markdown("""
### 🖥️ Para o Monitor (Tela Pública)
**Clique em '1 Monitor'** na Barra Lateral em uma tela separada.
""")

st.warning("⚠️ Se a barra lateral estiver recolhida, clique no ícone **>** (seta) no canto superior esquerdo para expandi-la e ver os links.")
