import streamlit as st
import time

# --- Configurações e Inicialização Global ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê Unificado")

# --- Variáveis de Lógica ---
PREFIXO = 'A'
GUICHES_DISPONIVEIS = [10, 20, 30, 40]

# 🔑 Variável de Controle de Visualização
# Inicializa a vista para o menu
if 'view' not in st.session_state:
    st.session_state.view = 'menu'
    
# --- Inicialização de Estado do Guichê (Apenas uma vez) ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- CSS Único para Todo o App ---
st.markdown("""
    <style>
    /* CSS para o Menu Inicial */
    .menu-box {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    /* CSS para o Monitor */
    .big-font-senha {
        font-size: 150px !important; font-weight: 900; color: #e74c3c; text-align: center; padding-top: 20px;
    }
    .big-font-vaga {
        font-size: 100px !important; font-weight: 900; color: #3498db; text-align: center; padding-top: 20px;
    }
    .monitor-box-page {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        text-align: center; height: 350px; display: flex; flex-direction: column; justify-content: center;
    }
    /* CSS para Atendente */
    .stButton>button {
        width: 100%; height: 100px; font-size: 24px; background-color: #2ecc71; color: white; border-radius: 10px; margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


# --- Funções de Lógica ---
def formatar_senha(numero):
    return f"{PREFIXO}-{numero}"

def chamar_senha(vaga_chamada):
    st.session_state.senha_atual += 1
    nova_senha_formatada = formatar_senha(st.session_state.senha_atual)
    
    st.session_state.vaga_atual = str(vaga_chamada)
    st.session_state.ultima_chamada_display = nova_senha_formatada
    
    st.toast(f"🔔 Chamando: {nova_senha_formatada} na VAGA {vaga_chamada}", icon="✅")

# ==========================================================
## 1. Módulo Monitor (Visão do Cliente)
# ==========================================================
def view_monitor():
    st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

    col_senha, col_vaga = st.columns(2)

    with col_senha:
        st.markdown('<div class="monitor-box-page" style="background-color: #ffe0e0;"><h3>SENHA CHAMADA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{st.session_state.ultima_chamada_display}</p>', unsafe_allow_html=True)

    with col_vaga:
        st.markdown('<div class="monitor-box-page" style="background-color: #e0f2ff;"><h3>DIRIJA-SE AO GUICHÊ</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{st.session_state.vaga_atual}</p>', unsafe_allow_html=True)

    # Força a atualização da página a cada 1 segundo (Polling)
    time.sleep(1) 
    st.experimental_rerun()

# ==========================================================
## 2. Módulo Atendente (Controle)
# ==========================================================
def view_atendente():
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
                st.experimental_rerun() # Necessário para atualizar o display de info
            
    st.markdown("---")
    if st.button("Voltar ao Menu", key="back_menu"):
        st.session_state.view = 'menu'
        st.experimental_rerun()

# ==========================================================
## 3. Módulo Menu (Inicial)
# ==========================================================
def view_menu():
    st.title("Sistema de Guichê: Escolha seu Modo")
    st.markdown("---")
    st.header("Qual é a sua função nesta tela?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="menu-box" style="background-color: #e0f2ff;"><h3>TELA DO CLIENTE</h3></div>', unsafe_allow_html=True)
        if st.button("Sou MONITOR", key="btn_monitor", type="primary"):
            st.session_state.view = 'monitor'
            st.experimental_rerun() 

    with col2:
        st.markdown('<div class="menu-box" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
        if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
            st.session_state.view = 'atendente'
            st.experimental_rerun() 

    st.markdown("---")
    st.caption("Acesse a mesma URL em telas diferentes e selecione os modos.")

# ==========================================================
## 4. Roteador Principal (Execução)
# ==========================================================

# O Streamlit executa o código do topo para baixo. 
# O roteador decide qual função chamar com base no estado.

if st.session_state.view == 'monitor':
    view_monitor()
elif st.session_state.view == 'atendente':
    view_atendente()
else:
    # 'menu' é o padrão
    view_menu()
