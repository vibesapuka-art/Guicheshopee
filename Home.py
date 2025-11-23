import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# CSS para esconder a barra lateral na Home Page
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

# --- Inicialização Global do Estado (Necessária para Home.py) ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- Funções de Navegação JavaScript ---

def redirect_to_page(page_name):
    """Injeta JavaScript para redirecionar o navegador."""
    # O Streamlit nomeia as páginas usando o slug do nome do arquivo (ex: Monitor, Atendente)
    js = f"""
        <script>
            window.location.href = "{page_name}";
        </script>
    """
    st.markdown(js, unsafe_allow_html=True)


# --- Layout da Home Page ---
st.title("Sistema de Guichê: Escolha seu Modo")
st.markdown("---")
st.header("Qual é a sua função nesta tela?")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="monitor-box-home" style="background-color: #e0f2ff;"><h3>TELA DO CLIENTE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 Ação: Chama a função JavaScript (redirect_to_page)
    if st.button("Sou MONITOR", key="btn_monitor", type="primary"):
        # O nome do arquivo no Streamlit Cloud é: NomeDaPagina (sem números ou .py)
        redirect_to_page("Monitor") 

with col2:
    st.markdown('<div class="monitor-box-home" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 Ação: Chama a função JavaScript (redirect_to_page)
    if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
        redirect_to_page("Atendente") 
        
st.markdown("---")
st.caption("Acesse a mesma URL em telas diferentes para sincronizar. O sistema agora usa páginas separadas.")
