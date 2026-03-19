import streamlit as st
import requests

# Configurações visuais da página
st.set_page_config(layout="wide", page_title="Monitor de Rastreabilidade")

# Seu link do Firebase
URL_FIREBASE = "https://rastreio-b7fb8-default-rtdb.firebaseio.com/pedidos.json"

st.title("📊 Monitor de Rastreabilidade de Pedidos")

# Botão para o chefe atualizar a tela e puxar os dados mais novos da nuvem
col_titulo, col_botao = st.columns([8, 1])
with col_botao:
    if st.button("🔄 Atualizar"):
        st.rerun()

# Busca os dados no Firebase
try:
    resposta = requests.get(URL_FIREBASE)
    dados = resposta.json()
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")
    dados = None

# Constrói a tela se existirem dados
if dados:
    obra_selecionada = st.selectbox("Selecione a Obra para visualizar:", list(dados.keys()))

    col1, col2, col3, col4 = st.columns(4)
    fases = ["RM", "SC", "OC", "OCFINALIZADA"]
    colunas_st = [col1, col2, col3, col4]

    st.markdown("---")

    for i, fase in enumerate(fases):
        with colunas_st[i]:
            st.markdown(f"### {fase}")
            for pedido in dados[obra_selecionada].get(fase, []):

                numero = pedido.get('numero', '')
                g_val = pedido.get('g', 'G3')
                obs = pedido.get('obs', '')
                logistica = pedido.get('logistica', '')

                # Exibe a etiqueta G3/G4 apenas na coluna OC, igual ao seu programa
                if fase == "OC":
                    st.info(f"**ID:** {numero} &nbsp;|&nbsp; **{g_val}**\n\n**Obs:** {obs}\n\n**Status:** {logistica}")
                else:
                    st.info(f"**ID:** {numero}\n\n**Obs:** {obs}\n\n**Status:** {logistica}")
else:
    st.warning("O banco de dados está vazio no momento.")