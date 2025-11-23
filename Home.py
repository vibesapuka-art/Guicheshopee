import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

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

# --- Inicialização Global do Estado ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- Funções de Navegação JavaScript Corrigidas ---

def redirect_to_page(path):
    """Injeta JavaScript para redirecionar para o caminho da página alvo."""
    # Obter o caminho base atual (ex: /app-name)
    base_path = st.get_option('server.baseUrlPath')
    
    # Criar a URL completa de destino
    full_url = f"{base_path}/{path}"

    js = f"""
        <script>
            window.location.href = "{full_url}";
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
    
    # 🟢 Ação: Chama a função JavaScript com o nome do arquivo da página de destino
    if st.button("Sou MONITOR", key="btn_monitor", type="primary"):
        # O Streamlit cria o slug do arquivo pages/1_Monitor.py como Monitor
        redirect_to_page("Monitor") 

with col2:
    st.markdown('<div class="monitor-box-home" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
    
    # 🟢 Ação: Chama a função JavaScript com o nome do arquivo da página de destino
    if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
        # O Streamlit cria o slug do arquivo pages/2_Atendente.py como Atendente
        redirect_to_page("Atendente") 
        
st.markdown("---")
st.caption("Acesse a mesma URL em telas diferentes para sincronizar. Você só precisa clicar no botão uma vez por tela.")
