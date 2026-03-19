import streamlit as st
import requests

# Configurações da página (Layout expansivo e ícone no navegador)
st.set_page_config(layout="wide", page_title="Monitor de Obras", page_icon="🏗️")

# Seu link do Firebase
URL_FIREBASE = "https://rastreio-b7fb8-default-rtdb.firebaseio.com/pedidos.json"

# Injeta um pouco de CSS para deixar o fundo das colunas levemente cinza (estilo Trello)
st.markdown("""
    <style>
    [data-testid="column"] {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Rastreabilidade")

# Botão de atualização
col_titulo, col_botao = st.columns([8, 1])
with col_botao:
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.rerun()

# Busca os dados no Firebase
try:
    resposta = requests.get(URL_FIREBASE)
    dados = resposta.json()
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")
    dados = None

if dados:
    st.markdown("---")
    # Seleção da obra com destaque
    obra_selecionada = st.selectbox("🏢 Selecione a Obra para visualizar:", list(dados.keys()))
    dados_obra = dados[obra_selecionada]

    # -------------------------------------------------------------
    # NOVO: Painel de Indicadores (Métricas) no topo
    # -------------------------------------------------------------
    st.markdown("### Resumo de Pedidos")
    metrica1, metrica2, metrica3, metrica4 = st.columns(4)
    metrica1.metric("Total em RM", len(dados_obra.get("RM", [])))
    metrica2.metric("Total em SC", len(dados_obra.get("SC", [])))
    metrica3.metric("Total em OC", len(dados_obra.get("OC", [])))
    metrica4.metric("OC Finalizada", len(dados_obra.get("OCFINALIZADA", [])))

    st.markdown("---")

    # -------------------------------------------------------------
    # NOVO: Layout Kanban com Cartões Modernos
    # -------------------------------------------------------------
    fases = ["RM", "SC", "OC", "OCFINALIZADA"]
    cores_fases = {"RM": "🔵", "SC": "🟠", "OC": "🟣", "OCFINALIZADA": "🟢"}

    colunas_st = st.columns(4)

    for i, fase in enumerate(fases):
        with colunas_st[i]:
            # Cabeçalho da coluna com ícone de cor
            st.markdown(f"#### {cores_fases[fase]} {fase}")

            # Desenha os cartões
            for pedido in dados_obra.get(fase, []):
                numero = pedido.get('numero', '')
                g_val = pedido.get('g', 'G3')
                obs = pedido.get('obs', '')
                logistica = pedido.get('logistica', '')

                # Container cria o efeito visual de um "Cartão" isolado
                with st.container(border=True):
                    if fase == "OC":
                        st.markdown(f"**ID:** {numero} &nbsp;|&nbsp; `{g_val}`")
                    else:
                        st.markdown(f"**ID:** {numero}")

                    st.markdown(f"📝 {obs}")

                    # Status em vermelho brilhante usando sintaxe do Streamlit
                    if logistica:
                        st.markdown(f":red[**Status:** {logistica}]")

else:
    st.warning("O banco de dados está vazio no momento.")