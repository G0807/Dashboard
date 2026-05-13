import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl

# O 'r' antes das aspas resolve o problema instantaneamente
#df = pd.read_excel(r'C:\Users\COMPUTADOR\Desktop\Jupyter\.venv\Base_vendas.xlsx')
#print(df)
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração para o Streamlit usar a largura total da tela
st.set_page_config(layout="wide")

st.title("📊 Meu Primeiro Dashboard de Vendas")

# 1. Leitura do arquivo (usando o caminho que você confirmou que funciona)
df = pd.read_excel('Base_vendas.xlsx')
# Remove espaços invisíveis no início ou fim de todos os nomes de colunas
df.columns = df.columns.str.strip()

# 2. Tratamento de Dados (A sua regra de ouro para garantir exatidão)
# Criando a coluna Vendedor para não confundir pessoas com o mesmo nome
df['Vendedor'] = df['Primeiro Nome'] + ' ' + df['Sobrenome']

# 3. Exibindo os dados no Navegador
st.subheader("Visualização da Base de Dados")
st.dataframe(df) # Cria uma tabela interativa que permite ordenar e filtrar

# 4. Criando um gráfico simples para testar o visual
st.subheader("Total de Vendas por Categoria")
vendas_por_cat = df.groupby('Categoria')['total de vendas'].sum().reset_index()

fig = px.bar(vendas_por_cat, x='Categoria', y='total de vendas', 
             title="Vendas por Categoria",
             color_discrete_sequence=['#00CC96'])

st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Vendas Pro", layout="wide")

# 2. CARREGAMENTO E LIMPEZA (Sempre com cache para performance)
@st.cache_data
def carregar_dados():
    # Usando o caminho que funcionou na sua máquina
    caminho = r'C:\Users\COMPUTADOR\Desktop\Jupyter\.venv\Base_vendas.xlsx'
    df = pd.read_excel(caminho)
    
    # Limpeza de nomes de colunas (para evitar o KeyError que resolvemos)
    df.columns = df.columns.str.strip()
    
    # Lógica de Exatidão: Unificar Nome + Sobrenome para garantir unicidade
    df['Vendedor_Completo'] = df['Primeiro Nome'].astype(str) + ' ' + df['Sobrenome'].astype(str)
    
    # Garantir que a data é um objeto de tempo
    df['Data'] = pd.to_datetime(df['Data'])
    
    return df

df = carregar_dados()

# 3. TÍTULO E FILTROS LATERAIS
st.title("🚀 Painel Analítico de Vendas")
st.markdown("---")

st.sidebar.header("Painel de Filtros")
filtro_loja = st.sidebar.multiselect("Selecione a Loja/Região", options=df['Loja'].unique(), default=df['Loja'].unique())
filtro_cat = st.sidebar.multiselect("Selecione a Categoria", options=df['Categoria'].unique(), default=df['Categoria'].unique())

# Aplicando os filtros
df_view = df[df['Loja'].isin(filtro_loja) & df['Categoria'].isin(filtro_cat)]

# 4. CRIAÇÃO DAS ABAS (Como solicitado no projeto original)
aba_dash, aba_tabelas, aba_base = st.tabs(["📊 Dashboards", "📈 Tabelas Dinâmicas", "📂 Base de Vendas"])

# --- ABA 1: DASHBOARDS ---
with aba_dash:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 1: Total de vendas por categoria
        vendas_cat = df_view.groupby('Categoria')['total de vendas'].sum().reset_index()
        fig1 = px.bar(vendas_cat, x='Categoria', y='total de vendas', title="Vendas por Categoria", color='Categoria')
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Desempenho por região (Lojas)
        vendas_loja = df_view.groupby('Loja')['total de vendas'].sum().reset_index()
        fig2 = px.pie(vendas_loja, names='Loja', values='total de vendas', title="Desempenho por Região", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Gráfico 3: Gráfico Temporal (Vendas ao longo do tempo)
        vendas_tempo = df_view.groupby('Data')['total de vendas'].sum().reset_index().sort_values('Data')
        fig3 = px.line(vendas_tempo, x='Data', y='total de vendas', title="Evolução Temporal das Vendas")
        st.plotly_chart(fig3, use_container_width=True)
        
        # Gráfico 4: Top 10 Vendedores (Garantindo que 'Fulano Silva' != 'Fulano Oliveira')
        top_vendedores = df_view.groupby('Vendedor_Completo')['total de vendas'].sum().nlargest(10).reset_index()
        fig4 = px.bar(top_vendedores, x='total de vendas', y='Vendedor_Completo', orientation='h', title="Top 10 Vendedores", color='total de vendas')
        st.plotly_chart(fig4, use_container_width=True)

# --- ABA 2: TABELAS ---
with aba_tabelas:
    st.subheader("Resumo Consolidado (Tabelas Dinâmicas)")
    # Simulando a "Tabela Dinâmica" do Excel com agrupamentos
    metricas = df_view.groupby(['Loja', 'Categoria']).agg({'total de vendas': 'sum', 'Quantidade Vendida': 'sum'}).reset_index()
    st.dataframe(metricas, use_container_width=True)
    
    st.download_button(label="Baixar Resumo em CSV", data=metricas.to_csv(index=False), file_name="resumo_vendas.csv", mime="text/csv")

# --- ABA 3: BASE DE VENDAS ---
with aba_base:
    st.subheader("Dados Brutos Tratados")
    st.markdown("Esta aba contém a base original com o cruzamento de nomes já realizado.")
    st.dataframe(df_view, use_container_width=True)

