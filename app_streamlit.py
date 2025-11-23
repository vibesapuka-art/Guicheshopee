import streamlit as st
import time

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

# Inicialização do estado da sessão
if 'senha_atual' not in st.session_state:
    st.session_state.senha_atual = 'A-0'
if 'vaga_atual' not in st.session_state:
    st.session_state.vaga_atual = '---'
if 'ultima_chamada' not in st.session_state:
    st.session_state.ultima_chamada = 'A-0'
    
# Variáveis de Controle
guiches_disponiveis = [10, 20, 30, 40]
prefixo = 'A'
contador = 0

# Função para formatar o número da senha
def incrementar_senha():
    global contador
    partes = st.session_state.senha_atual.split('-')
    if len(partes) == 2 and partes[0] == prefixo:
        try:
            contador = int(partes[1]) + 1
        except ValueError:
            contador = 1
    
    st.session_state.senha_atual = f"{prefixo}-{contador}"
    return st.session_state.senha_atual

# Função que é chamada ao clicar no botão
def chamar_senha(vaga_chamada):
    nova_senha = incrementar_senha()
    st.session_state.vaga_atual = str(vaga_chamada)
    st.session_state.ultima_chamada = nova_senha # Atualiza a última chamada
    st.toast(f"Chamando: {nova_senha} na VAGA {vaga_chamada}", icon="🔔")

# --- Interface Principal ---

# 1. Recuperar o parâmetro da URL para saber qual tela exibir
query_params = st.query_params

if 'view' in query_params and query_params['view'][0] == 'monitor':
    ## --- 🖥️ Tela do Monitor (Visão do Cliente) ---
    st.markdown("""
        <style>
        .big-font-senha {
            font-size: 150px !important;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
        }
        .big-font-vaga {
            font-size: 100px !important;
            font-weight: bold;
            color: #3498db;
            text-align: center;
        }
        .monitor-box {
            padding: 30px;
            margin: 20px 0;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.header("🔔 Painel de Chamada")

    col_senha, col_vaga = st.columns(2)

    with col_senha:
        st.markdown('<div class="monitor-box" style="background-color: #fcebeb;"><h3>SENHA CHAMADA</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-senha">{st.session_state.ultima_chamada}</p>', unsafe_allow_html=True)

    with col_vaga:
        st.markdown('<div class="monitor-box" style="background-color: #ebf5fb;"><h3>DIRIJA-SE AO GUICHÊ</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="big-font-vaga">{st.session_state.vaga_atual}</p>', unsafe_allow_html=True)

    # Função para forçar a atualização (Reload automático)
    time.sleep(1) 
    st.experimental_rerun() # Faz a página recarregar a cada segundo para buscar o novo estado

else:
    ## --- 🎛️ Tela do Atendente (Visão do Guichê) ---
    st.title("Sistema de Chamada de Guichê")
    st.subheader(f"Última Senha Chamada: **{st.session_state.ultima_chamada}** na Vaga **{st.session_state.vaga_atual}**")
    
    st.markdown("---")

    st.subheader("Selecione sua Vaga/Guichê:")

    cols = st.columns(len(guiches_disponiveis))

    for i, vaga in enumerate(guiches_disponiveis):
        with cols[i]:
            if st.button(f"Guichê {vaga}", key=f"btn_{vaga}"):
                # Chama a função para incrementar e atualizar a sessão
                chamar_senha(vaga)
    
    st.markdown("---")
    st.info(f"""
    **Instruções:**
    1. Abra esta página e use os botões acima para chamar a próxima senha.
    2. Diga aos clientes para acessarem o painel do monitor em: 
       `{st.get_option('server.baseUrlPath')}?view=monitor`
    """)
