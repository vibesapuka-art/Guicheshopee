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

# --- CSS Único para Todo o App (AJUSTADO PARA VISIBILIDADE DO MONITOR) ---
st.markdown("""
    <style>
    /* CSS para o Menu Inicial */
    .menu-box {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    
    /* CSS para o Monitor */
    /* Tamanho de Fonte MAIOR para a Senha */
    .big-font-senha {
        font-size: 180px !important; font-weight: 900; color: #e74c3c; text-align: center; padding-top: 20px;
        line-height: 1.1;
    }
    /* Tamanho de Fonte MAIOR para a Gaiola */
    .big-font-vaga {
        font-size: 130px !important; font-weight: 900; color: #3498db; text-align: center; padding-top: 20px;
        line-height: 1.1;
    }
    .monitor-box-page {
        padding: 40px; margin: 10px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        text-align: center; height: auto; display: flex; flex-direction: column; justify-content: center;
    }
    
    /* Outros CSS */
    .stButton>button {
        width: 100%; height: 100px; font-size: 24px; background-color: #2ecc71; color: white; border-radius: 10px; margin: 10px 0;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .css-vk3250 {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
## Funções de Estado Compartilhado com Histórico
# ==========================================================

def read_shared_state():
    """Lê o estado compartilhado do arquivo de texto, incluindo o histórico."""
    if not os.path.exists(STATE_FILE):
        # Retorna o estado inicial se o arquivo não existir
        return {'senha_display': 'A-0', 'vaga': 'GAIOLA ---', 'senha_num': 0, 'history': []} 
        
    with open(STATE_FILE, "r") as f:
        try:
            lines = [line.strip() for line in f.readlines()]
            if len(lines) < 3:
                 return {'senha_display': 'A-0', 'vaga': 'GAIOLA ---', 'senha_num': 0, 'history': []}
                 
            senha_display = lines[0]
            vaga = lines[1]
            senha_num = int(lines[2])
            # O histórico começa da linha 3 em diante (formato: Senha|Gaiola)
            history = [item.split('|') for item in lines[3:] if '|' in item]
            return {'senha_display': senha_display, 'vaga': vaga, 'senha_num': senha_num, 'history': history}
        except:
            return {'senha_display': 'A-0', 'vaga': 'GAIOLA ---', 'senha_num': 0, 'history': []}

def write_shared_state(senha_display, vaga, senha_num, history):
    """Escreve o estado compartilhado no arquivo de texto, incluindo o histórico."""
    with open(STATE_FILE, "w") as f:
        # 1. Estado Atual
        f.write(f"{senha_display}\n")
        f.write(f"{vaga}\n")
        f.write(f"{senha_num}\n")
        # 2. Histórico (limitado a 10)
        for item in history:
            f.write(f"{item[0]}|{item[1]}\n")

# --- Funções de Lógica ---
def chamar_senha(senha_completa, vaga_selecionada):
    """Atualiza o estado compartilhado com a senha e vaga selecionadas, e gerencia o histórico."""
    
    # Define o que será exibido no Monitor (VAGA X -> GAIOLA X)
    vaga_display = vaga_selecionada.replace("VAGA", "GAIOLA")
    
    # 1. Lê o estado anterior (incluindo o histórico)
    estado_anterior = read_shared_state()
    history = estado_anterior['history']

    # 2. Adiciona a nova chamada ao TOPO do histórico
    novo_item_historico = [senha_completa, vaga_display]
    # Se a chamada atual for diferente da última registrada (para evitar duplicidade imediata)
    if not history or history[0] != novo_item_historico:
        history.insert(0, novo_item_historico)
    
    # 3. Limita o histórico às últimas 10 chamadas (a atual e mais 9 anteriores)
    history = history[:10]
    
    # 4. Atualiza o estado local do Atendente
    st.session_state.vaga_atual = vaga_selecionada 
    st.session_state.ultima_chamada_display = senha_completa
    
    # 5. ESCREVE o novo estado no arquivo compartilhado
    write_shared_state(senha_completa, vaga_display, 0, history) 
    
    st.toast(f"🔔 Chamando: {senha_completa} na {vaga_selecionada}", icon="✅") 


# ==========================================================
## 1. Módulo Monitor (Visão do Cliente - NOVO LAYOUT)
# ==========================================================
def view_monitor():
    # 1. LÊ o estado mais atual do arquivo compartilhado
    estado_compartilhado = read_shared_state()
    
    st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

    # Nova estrutura de colunas: Grande para a Chamada Atual, Pequena para o Histórico
    col_chamada_atual, col_historico = st.columns([3, 1])

    # --- COLUNA MAIOR: CHAMADA ATUAL (Mais Visível) ---
    with col_chamada_atual:
        st.subheader("CHAMADA ATUAL")
        
        # Senha Atual
        st.markdown('<div class="monitor-box-page" style="background-color: #ffe0e0; padding: 20px;"><h3>SENHA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{estado_compartilhado["senha_display"]}</p>', unsafe_allow_html=True)

        # Gaiola Atual (Renomeado)
        st.markdown('<div class="monitor-box-page" style="background-color: #e0f2ff; padding: 20px;"><h3>DIRIJA-SE À</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{estado_compartilhado["vaga"]}</p>', unsafe_allow_html=True)

    # --- COLUNA MENOR: HISTÓRICO DAS ÚLTIMAS 10 ---
    with col_historico:
        st.subheader("Últimas Chamadas")
        
        history_data = estado_compartilhado.get('history', [])
        
        if history_data:
            # A chamada atual já está em destaque, então removemos a primeira para a lista de histórico
            # Usamos [:9] para mostrar as 9 anteriores, totalizando 10 visíveis.
            history_for_display = history_data[1:] 

            data_for_display = []
            for item in history_for_display:
                data_for_display.append({
                    "Senha": item[0],
                    "Gaiola": item[1]
                })
                
            st.dataframe(
                data_for_display, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Senha": st.column_config.TextColumn(width="small"),
                    "Gaiola": st.column_config.TextColumn(width="small")
                }
            )
        else:
            st.info("Nenhuma chamada anterior.")

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

    # Display da Última Chamada (Usa "vaga" para manter consistência com a seleção do Atendente)
    st.subheader(f"Última Chamada: **{estado_atual['senha_display']}** na **{estado_atual['vaga']}**")
    st.markdown("---")

    
    # --- SELETORES DE SENHA (LETRA + NÚMERO) ---
    st.subheader("1. Selecione a Senha para Chamada")
    col_letra, col_numero = st.columns(2)
    
    with col_letra:
        selected_letra = st.selectbox(
            "Selecione a Letra:",
            LETRAS_DISPONIVEIS,
            key="select_letra"
        )

    with col_numero:
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
    
    # Atendente ainda seleciona "VAGA X", e o sistema converte para "GAIOLA X" no Monitor
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
