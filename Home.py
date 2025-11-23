import streamlit as st
import time
import os

# --- Configurações e Variáveis ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê Unificado")

# --- Variáveis de Lógica ---
STATE_FILE = "guiche_state.txt" 
LETRAS_DISPONIVEIS = [chr(i) for i in range(ord('A'), ord('Z') + 1)] # A até Z
NUMEROS_DISPONIVEIS = list(range(1, 31)) # 1 até 30
VAGAS_DISPONIVEIS = [f"VAGA {i}" for i in range(1, 21)] # Vaga 1 até Vaga 20

# 🔑 Inicialização de Estado de Controle e Variáveis
if 'view' not in st.session_state:
    st.session_state.view = 'menu'
    
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
    /* Esconde barra lateral e menu */
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
## Funções de Estado Compartilhado (Sincronia entre Monitores e Atendentes)
# ==========================================================

def read_shared_state():
    """Lê o estado compartilhado do arquivo de texto."""
    if not os.path.exists(STATE_FILE):
        # Retorna o estado inicial se o arquivo não existir
        return {'senha_display': 'A-0', 'vaga': '---', 'senha_num': 0} 
        
    with open(STATE_FILE, "r") as f:
        try:
            lines = f.readlines()
            # O arquivo armazena: ultima_chamada_display, vaga_atual, senha_atual (senha_num)
            senha_display = lines[0].strip()
            vaga = lines[1].strip()
            # Mantemos senha_num para compatibilidade, mas agora será sempre 0
            senha_num = int(lines[2].strip()) 
            return {'senha_display': senha_display, 'vaga': vaga, 'senha_num': senha_num}
        except:
            return {'senha_display': 'A-0', 'vaga': '---', 'senha_num': 0}

def write_shared_state(senha_display, vaga, senha_num):
    """Escreve o estado compartilhado no arquivo de texto."""
    with open(STATE_FILE, "w") as f:
        f.write(f"{senha_display}\n")
        f.write(f"{vaga}\n")
        f.write(f"{senha_num}\n")

# --- Funções de Lógica ---
def chamar_senha(senha_completa, vaga_chamada):
    """Atualiza o estado compartilhado com a senha e vaga selecionadas."""
    
    # Atualiza o estado da sessão local (para o Atendente)
    st.session_state.vaga_atual = vaga_chamada
    st.session_state.ultima_chamada_display = senha_completa
    
    # ESCREVE o novo estado no arquivo compartilhado (senha_num é 0, pois a contagem é manual)
    write_shared_state(senha_completa, st.session_state.vaga_atual, 0)
    
    st.toast(f"🔔 Chamando: {senha_completa} na {vaga_chamada}", icon="✅")


# ==========================================================
## 1. Módulo Monitor (Visão do Cliente)
# ==========================================================
def view_monitor():
    # 1. LÊ o estado mais atual do arquivo compartilhado
    estado_compartilhado = read_shared_state()
    
    st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

    col_senha, col_vaga = st.columns(2)

    with col_senha:
        st.markdown('<div class="monitor-box-page" style="background-color: #ffe0e0;"><h3>SENHA CHAMADA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{estado_compartilhado["senha_display"]}</p>', unsafe_allow_html=True)

    with col_vaga:
        st.markdown('<div class="monitor-box-page" style="background-color: #e0f2ff;"><h3>DIRIJA-SE AO LOCAL</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{estado_compartilhado["vaga"]}</p>', unsafe_allow_html=True)

    # Força a atualização da página a cada 1 segundo (Polling)
    time.sleep(1) 
    st.rerun() 

# ==========================================================
## 2. Módulo Atendente (Controle - Seleção Manual)
# ==========================================================
def view_atendente():
    # 1. Lê o estado atual (local ou compartilhado)
    estado_atual = read_shared_state()
    
    st.title("Sistema de Chamada de Guichê")

    # Display da Última Chamada
    st.subheader(f"Última Chamada: **{estado_atual['senha_display']}** na **{estado_atual['vaga']}**")
    st.markdown("---")

    
    # --- SELETORES DE SENHA (LETRA + NÚMERO) ---
    st.subheader("1. Selecione a Senha para Chamada")
    col_letra, col_numero = st.columns(2)
    
    with col_letra:
        # Seletor de Letra
        selected_letra = st.selectbox(
            "Selecione a Letra:",
            LETRAS_DISPONIVEIS,
            key="select_letra"
        )

    with col_numero:
        # Seletor de Número
        selected_numero = st.selectbox(
            "Selecione o Número:",
            NUMEROS_DISPONIVEIS,
            key="select_numero"
        )
        
    senha_a_chamar = f"{selected_letra}{selected_numero}"
    st.metric(label="SENHA PRONTA", value=senha_a_chamar)
    
    st.markdown("---")

    # --- SELETOR DE VAGA (GUICHÊ) ---
    st.subheader("2. Selecione a Vaga (Guichê)")
    
    # Seletor de Vaga
    selected_vaga = st.selectbox(
        "Vaga de Destino:",
        VAGAS_DISPONIVEIS,
        key="select_vaga"
    )

    st.markdown("---")
    
    # --- BOTÃO DE CHAMADA FINAL ---
    st.subheader("3. Confirmar Chamada")
    if st.button(f"CHAMAR {senha_a_chamar} para {selected_vaga}", key="btn_chamar"):
        # Chama a função principal com as seleções
        chamar_senha(senha_a_chamar, selected_vaga)
        st.rerun() 
            
    st.markdown("---")
    if st.button("Voltar ao Menu", key="back_menu"):
        st.session_state.view = 'menu'
        st.rerun()

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
            st.rerun()

    with col2:
        st.markdown('<div class="menu-box" style="background-color: #ffe0e0;"><h3>TELA DE CONTROLE</h3></div>', unsafe_allow_html=True)
        if st.button("Sou ATENDENTE", key="btn_atendente", type="primary"):
            st.session_state.view = 'atendente'
            st.rerun()

    st.markdown("---")
    st.caption("Acesse a mesma URL em telas diferentes e selecione os modos.")

# ==========================================================
## 4. Roteador Principal (Execução)
# ==========================================================

if st.session_state.view == 'monitor':
    view_monitor()
elif st.session_state.view == 'atendente':
    view_atendente()
else:
    view_menu()
