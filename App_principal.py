import streamlit as st
import time

# --- Configuração e Inicialização do Estado ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# CSS para esconder a barra lateral e o menu de opções em todas as visualizações
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

# --- 1. Inicialização do Estado (Armazenamento Simples) ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'
    
# Variáveis de Configuração
PREFIXO = 'A'
GUICHES_DISPONIVEIS = [10, 20, 30, 40]

# --- 2. Funções de Lógica ---
def formatar_senha(numero):
    return f"{PREFIXO}-{numero}"

def chamar_senha(vaga_chamada):
    st.session_state.senha_atual += 1
    nova_senha_formatada = formatar_senha(st.session_state.senha_atual)
    
    st.session_state.vaga_atual = str(vaga_chamada)
    st.session_state.ultima_chamada_display = nova_senha_formatada
    
    st.toast(f"🔔 Chamando: {nova_senha_formatada} na VAGA {vaga_chamada}", icon="✅")

# --- 3. CSS para o Layout ---
st.markdown("""
    <style>
    /* Estilos do Monitor */
    .big-font-senha { font-size: 150px !important; font-weight: 900; color: #e74c3c; text-align: center; padding-top: 20px; }
    .big-font-vaga { font-size: 100px !important; font-weight: 900; color: #3498db; text-align: center; padding-top: 20px; }
    .monitor-box { padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); text-align: center; height: 350px; display: flex; flex-direction: column; justify-content: center; }
    /* Estilos dos Botões de Chamada */
    .stButton>button { width: 100%; height: 100px; font-size: 24px; border-radius: 10px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 4. Roteamento (Decide qual tela mostrar) ---

query_params = st.query_params
view_mode = query_params.get('view', [None])[0]
base_url = st.get_option('server.baseUrlPath') # Obtém a URL base para links

if view_mode == 'monitor':
    
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

    # Força a atualização da página a cada 1 segundo
    time.sleep(1) 
    st.experimental_rerun() 

elif view_mode == 'atendente':
    
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
    # Link de acesso rápido ao Monitor para referência
    st.markdown(f"""
    ### 🔗 Link para o Monitor (Tela Pública)
    **<a href="{base_url}?view=monitor" target="_blank">CLIQUE AQUI PARA ABRIR O MONITOR</a>**
    """, unsafe_allow_html=True)
    
else:
    # ==========================================================
    ## --- 🏠 Home Page (Escolha de Modo) ---
    # ==========================================================
    
    st.title("Sistema de Guichê: Escolha seu Modo")
    st.markdown("---")
    
    st.header("Qual é a sua função nesta tela?")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="monitor-box" style="background-color: #e0f2ff;"><h3>TELA DO CLIENTE</h3></div>', unsafe_allow_html=True)
        # Link HTML para redirecionar para o Monitor
        st.markdown(f'<a href="{base_url}?view=monitor" target="_self"><button style="background-color: #3498db; color: white; border: none;">Sou MONITOR</button></a>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="monitor-box" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
        # Link HTML para redirecionar para o Atendente
        st.markdown(f'<a href="{base_url}?view=atendente" target="_self"><button style="background-color: #2ecc71; color: white; border: none;">Sou ATENDENTE</button></a>', unsafe_allow_html=True)
            
    st.markdown("---")
    st.caption("Acesse a mesma URL em telas diferentes e clique na função desejada para sincronizar.")
