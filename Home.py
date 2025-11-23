import streamlit as st
import time
import os # Necessário para manipular o arquivo de estado

# --- Configurações e Inicialização Global ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê Unificado")

# --- Variáveis de Lógica ---
PREFIXO = 'A'
GUICHES_DISPONIVEIS = [10, 20, 30, 40]

# Nome do arquivo de estado (será criado na pasta do aplicativo)
STATE_FILE = "guiche_state.txt" 

# 🔑 Variável de Controle de Visualização
if 'view' not in st.session_state:
    st.session_state.view = 'menu'
    
# --- Inicialização de Estado Local (para evitar erros, mas não é usado para sincronia) ---
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 0 
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'

# --- CSS Único para Todo o App (Mantido) ---
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
        width: 100%; height: 100px; font-size: 24px; background-color: #2ecc71; /* Verde */ color: white; border-radius: 10px; margin: 10px 0;
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
## NOVAS FUNÇÕES DE ESTADO COMPARTILHADO
# ==========================================================

def read_shared_state():
    """Lê o estado compartilhado do arquivo de texto."""
    if not os.path.exists(STATE_FILE):
        return {'senha_display': 'A-0', 'vaga': '---', 'senha_num': 0}
        
    with open(STATE_FILE, "r") as f:
        try:
            lines = f.readlines()
            # O arquivo armazena: ultima_chamada_display, vaga_atual, senha_atual
            senha_display = lines[0].strip()
            vaga = lines[1].strip()
            senha_num = int(lines[2].strip())
            return {'senha_display': senha_display, 'vaga': vaga, 'senha_num': senha_num}
        except:
            # Em caso de arquivo corrompido, retorna o estado inicial
            return {'senha_display': 'A-0', 'vaga': '---', 'senha_num': 0}

def write_shared_state(senha_display, vaga, senha_num):
    """Escreve o estado compartilhado no arquivo de texto."""
    with open(STATE_FILE, "w") as f:
        # Escreve o estado em três linhas separadas
        f.write(f"{senha_display}\n")
        f.write(f"{vaga}\n")
        f.write(f"{senha_num}\n")

# --- Funções de Lógica ---

def formatar_senha(numero):
    return f"{PREFIXO}-{numero}"

def chamar_senha(vaga_chamada):
    # 1. Lê o último estado para saber qual é a próxima senha
    estado_anterior = read_shared_state()
    proxima_senha_num = estado_anterior['senha_num'] + 1
    
    nova_senha_formatada = formatar_senha(proxima_senha_num)
    
    # 2. Atualiza o estado da sessão local (para o Atendente)
    st.session_state.senha_atual = proxima_senha_num
    st.session_state.vaga_atual = str(vaga_chamada)
    st.session_state.ultima_chamada_display = nova_senha_formatada
    
    # 3. ESCREVE o novo estado no arquivo compartilhado
    write_shared_state(nova_senha_formatada, st.session_state.vaga_atual, proxima_senha_num)
    
    st.toast(f"🔔 Chamando: {nova_senha_formatada} na VAGA {vaga_chamada}", icon="✅")

# ==========================================================
## 1. Módulo Monitor (Visão do Cliente)
# ==========================================================
def view_monitor():
    # 1. LÊ o estado mais atual do arquivo compartilhado
    estado_compartilhado = read_shared_state()
    
    # 2. Atualiza o display do Monitor com o estado lido
    st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

    col_senha, col_vaga = st.columns(2)

    with col_senha:
        st.markdown('<div class="monitor-box-page" style="background-color: #ffe0e0;"><h3>SENHA CHAMADA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{estado_compartilhado["senha_display"]}</p>', unsafe_allow_html=True)

    with col_vaga:
        st.markdown('<div class="monitor-box-page" style="background-color: #e0f2ff;"><h3>DIRIJA-SE AO GUICHÊ</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{estado_compartilhado["vaga"]}</p>', unsafe_allow_html=True)

    # Força a atualização da página a cada 1 segundo (Polling)
    time.sleep(1) 
    st.rerun() 

# ==========================================================
## 2. Módulo Atendente (Controle)
# ==========================================================
def view_atendente():
    # 1. Lê o estado atual (local ou compartilhado)
    estado_atual = read_shared_state()
    
    # 2. Define o display local com base no estado compartilhado
    st.session_state.senha_atual = estado_atual['senha_num']
    st.session_state.ultima_chamada_display = estado_atual['senha_display']
    st.session_state.vaga_atual = estado_atual['vaga']

    st.title("Sistema de Chamada de Guichê")

    # Garante que a próxima senha exibida é baseada no estado compartilhado
    st.info(f"Próxima Senha a Chamar: **{formatar_senha(estado_atual['senha_num'] + 1)}**")
    st.subheader(f"Última Chamada: **{estado_atual['senha_display']}** na Vaga **{estado_atual['vaga']}**")

    st.markdown("---")

    st.subheader("Clique no seu Guichê para Chamar a Próxima Senha")

    cols = st.columns(len(GUICHES_DISPONIVEIS))

    for i, vaga in enumerate(GUICHES_DISPONIVEIS):
        with cols[i]:
            if st.button(f"Guichê {vaga}", key=f"btn_{vaga}"):
                chamar_senha(vaga)
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
