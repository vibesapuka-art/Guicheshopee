import streamlit as st

st.set_page_config(layout="wide", page_title="Sistema de Guichê", initial_sidebar_state="collapsed")

st.title("👋 Bem-vindo ao Sistema de Chamada de Guichê")
st.markdown("---")
st.header("Selecione sua função na barra lateral à esquerda.")

st.info("""
**Instruções de Uso:**
1.  **Atendente:** Clique em '2 Atendente' na barra lateral para chamar as senhas.
2.  **Monitor:** Abra esta mesma URL em uma TV ou monitor diferente e clique em '1 Monitor' para exibição pública.
""")
