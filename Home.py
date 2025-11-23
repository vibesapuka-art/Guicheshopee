import streamlit as st
import time
import os
import json 

# --- Configurações e Variáveis ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê Unificado")

# --- Variáveis de Lógica ---
STATE_FILE = "guiche_state.json" 
LETRAS_DISPONIVEIS = [chr(i) for i in range(ord('A'), ord('Z') + 1)] 
NUMEROS_DISPONIVEIS = list(range(1, 31)) # 1 até 30
GUICHES_DISPONIVEIS = [f"GUICHÊ {i}" for i in range(1, 21)]

# 🔑 Inicialização de Estado de Controle e Variáveis
if 'view' not in st.session_state:
    st.session_state.view = 'menu'
    
if 'letra_selecionada' not in st.session_state:
    st.session_state.letra_selecionada = 'A' # Novo estado para a letra atual


# --- CSS Único para Todo o App (NOVO: Container Rolável e Ajustes de Botões) ---
st.markdown("""
    <style>
    /* Estilos Gerais (Mantidos) */
    .menu-box {
        padding: 40px; margin: 20px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    .big-font-senha { font-size: 180px !important; font-weight: 900; color: #e74c3c; text-align: center; padding-top: 20px; line-height: 1.1; }
    .big-font-vaga { font-size: 130px !important; font-weight: 900; color: #3498db; text-align: center; padding-top: 20px; line-height: 1.1; }
    .monitor-box-page { padding: 40px; margin: 10px 0; border-radius: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); text-align: center; height: auto; display: flex; flex-direction: column; justify-content: center; }
    .stButton>button { width: 100%; height: 100px; font-size: 24px; background-color: #2ecc71; color: white; border-radius: 10px; margin: 10px 0; }
    [data-testid="stSidebar"], .css-vk3250 { display: none; }
    
    /* === ESTILOS PARA CHECKBOXES === */
    /* Checkbox Amarelo (Chamando) */
    .yellow-box label {
        background-color: #f1c40f !important; /* Amarelo */
        color: black !important;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
        height: 50px; /* Altura fixa para todos */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Checkbox Verde (Chamado) */
    .green-box label {
        background-color: #2ecc71 !important; /* Verde */
        color: white !important;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Checkbox Padrão (Não Chamado) */
    .default-box label {
        background-color: #333333; /* Cor neutra para o tema escuro */
        color: white;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* === NOVO CONTAINER ROLÁVEL === */
    /* Aplica rolagem e altura máxima ao container onde estão as senhas */
    .stContainerWithScroll {
        overflow-y: scroll;
        max-height: 400px; /* Altura máxima para o container */
        padding: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    </style>
""", unsafe_allow_html=True)

# ==========================================================
## Funções de Estado Compartilhado
# ==========================================================

def read_shared_state():
    """Lê o estado compartilhado do arquivo JSON."""
    default_state = {
        'senha_display': 'A-0',
        'vaga': 'GAIOLA ---',
        'history': [],
        'senhas_status': {} 
    }
    if not os.path.exists(STATE_FILE):
        return default_state
        
    with open(STATE_FILE, "r") as f:
        try:
            state = json.load(f)
            if 'senhas_status' not in state:
                state['senhas_status'] = {}
            return state
        except:
            return default_state

def write_shared_state(state):
    """Escreve o estado compartilhado no arquivo JSON."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

# --- Funções de Lógica ---
def chamar_senha(senha_completa, vaga_selecionada):
    """Atualiza o estado compartilhado com a senha, vaga e gerencia o histórico e cores."""
    
    vaga_display = vaga_selecionada.replace("GUICHÊ", "GAIOLA")
    
    estado_atual = read_shared_state()
    history = estado_atual['history']
    senhas_status = estado_atual['senhas_status']
    
    # 1. ATUALIZA STATUS DE CORES (Movendo o Status Amarelo anterior para Verde)
    for senha, status in list(senhas_status.items()):
        if status == 'yellow':
            senhas_status[senha] = 'green'

    # 2. Define a nova senha como AMARELA (Sendo Chamada)
    senhas_status[senha_completa] = 'yellow'
    
    # 3. ATUALIZA HISTÓRICO
    novo_item_historico = [senha_completa, vaga_display]
    if not history or history[0] != novo_item_historico:
        history.insert(0, novo_item_historico)
    history = history[:10]
    
    # 4. ESCREVE O NOVO ESTADO
    novo_estado = {
        'senha_display': senha_completa,
        'vaga': vaga_display,
        'history': history,
        'senhas_status': senhas_status
    }
    write_shared_state(novo_estado)
    
    st.toast(f"🔔 Chamando: {senha_completa} no {vaga_selecionada}", icon="✅") 


# ==========================================================
## 1. Módulo Monitor (Visão do Cliente)
# ==========================================================
def view_monitor():
    estado_compartilhado = read_shared_state()
    
    st.markdown("<h1>🔔 Painel de Chamada ao Cliente</h1>", unsafe_allow_html=True)

    col_chamada_atual, col_historico = st.columns([3, 1])

    # --- COLUNA MAIOR: CHAMADA ATUAL ---
    with col_chamada_atual:
        st.subheader("CHAMADA ATUAL")
        
        st.markdown('<div class="monitor-box-page" style="background-color: #ffe0e0; padding: 20px;"><h3>SENHA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{estado_compartilhado["senha_display"]}</p>', unsafe_allow_html=True)

        st.markdown('<div class="monitor-box-page" style="background-color: #e0f2ff; padding: 20px;"><h3>DIRIJA-SE À</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{estado_compartilhado["vaga"]}</p>', unsafe_allow_html=True)

    # --- COLUNA MENOR: HISTÓRICO DAS ÚLTIMAS 10 ---
    with col_historico:
        st.subheader("Últimas Chamadas")
        
        history_data = estado_compartilhado.get('history', [])
        
        if history_data:
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

    time.sleep(1) 
    st.rerun() 

# ==========================================================
## 2. Módulo Atendente (Controle - Grade Rolável)
# ==========================================================
def view_atendente():
    estado_atual = read_shared_state()
    senhas_status = estado_atual['senhas_status']
    
    st.title("Sistema de Chamada de Guichê")

    st.subheader(f"Última Chamada: **{estado_atual['senha_display']}** na **{estado_atual['vaga']}**")
    st.markdown("---")
    
    # --- 1. SELEÇÃO DE VAGA (GUICHÊ) ---
    col_guiche, col_letra_select = st.columns([3, 1])

    with col_guiche:
        st.subheader("1. Selecione o Guichê de Atendimento")
        selected_guiche = st.selectbox(
            "Guichê de Destino:",
            GUICHES_DISPONIVEIS,
            key="select_guiche"
        )
    
    # --- SELETOR DE LETRA ---
    with col_letra_select:
        st.subheader("Letra")
        # Armazena a letra selecionada no estado da sessão
        st.session_state.letra_selecionada = st.selectbox(
            "Filtrar por Letra:",
            LETRAS_DISPONIVEIS,
            index=LETRAS_DISPONIVEIS.index(st.session_state.letra_selecionada),
            key="select_letra"
        )
        letra_atual = st.session_state.letra_selecionada

    st.markdown("---")
    
    # --- 2. SELEÇÃO DE SENHAS (GRID ROLÁVEL) ---
    st.subheader(f"2. Senhas da Letra **{letra_atual}** (Selecione para Chamar)")
    
    # NOVO: Container rolável para minimizar espaço
    with st.container():
        st.markdown('<div class="stContainerWithScroll">', unsafe_allow_html=True)
        
        # Cria 4 colunas para a grade (30/4 = 7.5, vamos usar 8 linhas completas)
        NUM_COLUNAS = 4
        COLUNAS_LIST = st.columns(NUM_COLUNAS)
        
        senhas_a_chamar = []
        
        for numero in NUMEROS_DISPONIVEIS: # 1 a 30
            senha = f"{letra_atual}{numero}"
            
            # Determina a classe CSS (cor)
            status = senhas_status.get(senha, 'default') 
            
            # Calcula em qual coluna o checkbox vai
            col_index = (numero - 1) % NUM_COLUNAS
            
            with COLUNAS_LIST[col_index]:
                # Adiciona a classe CSS diretamente ao container do checkbox
                st.markdown(f'<div class="{status}-box">', unsafe_allow_html=True)
                
                # Criando o checkbox
                is_checked = st.checkbox(f"{senha}", key=f"chk_{senha}", value=(status == 'yellow'))
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if is_checked:
                    # Se o checkbox for marcado:
                    if status == 'green':
                        # Se já foi chamado (verde), o Atendente clicou para LIMPAR
                        estado_para_limpar = read_shared_state()
                        if senha in estado_para_limpar['senhas_status']:
                            del estado_para_limpar['senhas_status'][senha]
                        write_shared_state(estado_para_limpar)
                        
                        # Limpa o checkbox localmente e recarrega para sumir a cor
                        st.session_state[f"chk_{senha}"] = False
                        st.rerun() 
                        
                    elif status == 'default':
                        # Se for um status novo ou default, adiciona à lista para chamar
                        senhas_a_chamar.append(senha)

        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")

    # --- 3. BOTÃO DE CHAMADA FINAL ---
    if senhas_a_chamar:
        # Pega a primeira senha marcada para chamar
        senha_final = senhas_a_chamar[0]
        
        if st.button(f"CHAMAR: {senha_final} no {selected_guiche}", key="btn_chamar_final"):
            chamar_senha(senha_final, selected_guiche)
            st.rerun()
    else:
        st.info("Selecione uma senha no menu acima.")
            
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
