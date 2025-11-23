import streamlit as st
import time
import os
import json # Novo: Para ler/escrever o estado de cores de forma robusta

# --- Configurações e Variáveis ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê Unificado")

# --- Variáveis de Lógica ---
STATE_FILE = "guiche_state.json" # Mudando para JSON
LETRAS_DISPONIVEIS = [chr(i) for i in range(ord('A'), ord('Z') + 1)] 
NUMEROS_DISPONIVEIS = list(range(1, 31))
GUICHES_DISPONIVEIS = [f"GUICHÊ {i}" for i in range(1, 21)] # Guichê 1 até 20

# 🔑 Inicialização de Estado de Controle e Variáveis
if 'view' not in st.session_state:
    st.session_state.view = 'menu'

# Estado Local (mantido para evitar erros de inicialização)
if 'ultima_chamada_display' not in st.session_state:
    st.session_state.ultima_chamada_display = 'A-0'


# --- CSS Único para Todo o App (NOVO: Suporte a Cores dos Checkboxes) ---
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
    
    /* === NOVOS ESTILOS PARA CHECKBOXES === */
    /* Checkbox Amarelo (Chamando) */
    .st-ag .yellow-box label {
        background-color: #f1c40f !important; /* Amarelo */
        color: black !important;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
    }
    /* Checkbox Verde (Chamado) */
    .st-ag .green-box label {
        background-color: #2ecc71 !important; /* Verde */
        color: white !important;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
    }
    /* Checkbox Padrão (Não Chamado) */
    .st-ag .default-box label {
        background-color: #333333; /* Cor neutra para o tema escuro */
        color: white;
        border-radius: 8px;
        padding: 8px;
        transition: background-color 0.3s;
    }
    /* Ajuste para alinhar checkboxes */
    [data-testid="stCheckbox"] {
        margin: 5px 0;
        border-radius: 8px;
    }

    </style>
""", unsafe_allow_html=True)

# ==========================================================
## Funções de Estado Compartilhado (JSON - Mais robusto)
# ==========================================================

def read_shared_state():
    """Lê o estado compartilhado do arquivo JSON."""
    default_state = {
        'senha_display': 'A-0',
        'vaga': 'GAIOLA ---',
        'history': [],
        'senhas_status': {} # Novo: Dicionário para rastrear o status de cada senha (cores)
    }
    if not os.path.exists(STATE_FILE):
        return default_state
        
    with open(STATE_FILE, "r") as f:
        try:
            state = json.load(f)
            # Garante que chaves importantes existam
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
    # Itera sobre o dicionário e move a senha que estava amarela para verde (Chamada Concluída)
    for senha, status in list(senhas_status.items()):
        if status == 'yellow':
            senhas_status[senha] = 'green' # Muda a senha recém-chamada para verde

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
## 2. Módulo Atendente (Controle - Checkboxes e Cores)
# ==========================================================
def view_atendente():
    estado_atual = read_shared_state()
    senhas_status = estado_atual['senhas_status'] # Puxa o status das cores
    
    st.title("Sistema de Chamada de Guichê")

    # Display da Última Chamada
    st.subheader(f"Última Chamada: **{estado_atual['senha_display']}** na **{estado_atual['vaga']}**")
    st.markdown("---")
    
    # --- 1. SELEÇÃO DE VAGA (GUICHÊ) ---
    st.subheader("1. Selecione o Guichê de Atendimento")
    selected_guiche = st.selectbox(
        "Guichê de Destino:",
        GUICHES_DISPONIVEIS,
        key="select_guiche"
    )

    st.markdown("---")
    
    # --- 2. SELEÇÃO DE SENHAS (CHECKBOXES EM GRADE) ---
    st.subheader("2. Selecione a Senha para Chamar")
    
    # Cria a grade de 5 colunas para os checkboxes
    cols = st.columns(5)
    
    senhas_a_chamar = []
    
    # Loop para criar os checkboxes
    for i, letra in enumerate(LETRAS_DISPONIVEIS):
        for numero in NUMEROS_DISPONIVEIS:
            senha = f"{letra}{numero}"
            
            # Determina a classe CSS (cor)
            status = senhas_status.get(senha, 'default') # Padrão é sem cor
            css_class = f"{status}-box"

            # Usa a mesma lógica de distribuição em 5 colunas
            col_index = (i * len(NUMEROS_DISPONIVEIS) + (numero - 1)) % 5
            
            with cols[col_index]:
                # O checkbox é criado, e o label é embrulhado com a classe CSS
                if st.checkbox(f" {senha} ", key=f"chk_{senha}"):
                    # Se o checkbox for marcado:
                    
                    if status == 'green':
                        # Se já foi chamado (verde), o Atendente clicou para LIMPAR
                        estado_para_limpar = read_shared_state()
                        # Remove o status de cor e desmarca o checkbox localmente
                        if senha in estado_para_limpar['senhas_status']:
                            del estado_para_limpar['senhas_status'][senha]
                        write_shared_state(estado_para_limpar)
                        
                        # Limpa o checkbox e recarrega para sumir a cor
                        st.session_state[f"chk_{senha}"] = False
                        st.rerun() 
                        
                    elif status == 'yellow':
                        # Se já está em processo, apenas aguarda
                        pass
                    else:
                        # Se for um status novo ou default, adiciona à lista para chamar
                        senhas_a_chamar.append(senha)
    
    st.markdown("---")

    # --- 3. BOTÃO DE CHAMADA FINAL ---
    if senhas_a_chamar:
        # Pega a primeira senha da lista para chamar
        senha_final = senhas_a_chamar[0]
        
        if st.button(f"CHAMAR: {senha_final} no {selected_guiche}", key="btn_chamar_final"):
            chamar_senha(senha_final, selected_guiche)
            st.rerun() # Recarrega para atualizar a cor para amarelo
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
