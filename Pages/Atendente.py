import streamlit as st

# --- Configuração ---
st.set_page_config(layout="wide", page_title="Controle de Chamada")

# Variáveis de Configuração (Mantenha aqui)
PREFIXO = 'A'
GUICHES_DISPONIVEIS = [10, 20, 30, 40]

# --- 1. Inicialização do Estado ---
# Se o estado não existe, inicializa (o Streamlit gerencia a sincronia entre páginas)
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- Funções de Lógica ---
def formatar_senha(numero):
    return f"{PREFIXO}-{numero}"

def chamar_senha(vaga_chamada):
    st.session_state.senha_atual += 1
    nova_senha_formatada = formatar_senha(st.session_state.senha_atual)
    
    st.session_state.vaga_atual = str(vaga_chamada)
    st.session_state.ultima_chamada_display = nova_senha_formatada
    
    st.toast(f"🔔 Chamando: {nova_senha_formatada} na VAGA {vaga_chamada}", icon="✅")

# --- CSS (Mantenha o CSS da versão anterior aqui) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 24px;
        background-color: #2ecc71; /* Verde */
        color: white;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
## --- 🎛️ Tela do Atendente (Visão do Guichê) ---
# ==========================================================

st.title("Sistema de Chamada de Guichê")

st.info(f"Próxima Senha a Chamar: **{formatar_senha(st.session_state.senha_atual + 1)}**")
st.subheader(f"Última Chamada: **{st.session_state.ultima_chamada_display}** na Vaga **{st.session_state.vaga_atual}**")

st.markdown("---")

st.subheader("Clique no seu Guichê para Chamar a Próxima Senha")

cols = st.columns(len(GUICHES_DISPONIVEIS))

for i, vaga in enumerate(GUICHES_DISPONIVEIS):
    with cols[i]:
        if st.button(f"Guichê {vaga}", key=f"btn_{vaga}"):
            chamar_senha(vaga)
            
st.markdown("---")
st.markdown("A **Barra Lateral** à esquerda permite alternar entre as páginas. Mantenha a página do Monitor aberta em outra tela.")
