import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados da planilha
file_path = "dados_filtrados_agrupados_bairrosfinal.xlsx"
df = pd.read_excel(file_path)

# Converter colunas de decimal para porcentagem
colunas_percentuais = ["PROP_LIXO/DOM", "PROP_SANEAMENTO/DOM", "PROP_AGUA/DOM"]
for coluna in colunas_percentuais:
    if coluna in df.columns:
        df[coluna] = df[coluna] * 100
        df[coluna] = df[coluna].map(lambda x: f"{x:.2f}%")

# Criar uma versão formatada da coluna de renda para exibição na tabela
coluna_monetaria = "RESP_RENDA_MEDIA"
if coluna_monetaria in df.columns:
    df["RESP_RENDA_FORMATADA"] = df[coluna_monetaria].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Título do aplicativo
st.title("📊 Visualização da Planilha Excel")

# Criar filtros interativos dentro do menu
with st.expander("🔽 Configurações de Filtros"):
    coluna_filtro = st.selectbox("Selecione a Coluna para Filtrar", df.columns)
    valores_unicos = df[coluna_filtro].unique()
    valor_selecionado = st.multiselect("Escolha os Valores", valores_unicos, default=valores_unicos.tolist())
    
    # Aplicar os filtros apenas se houver seleção
    if valor_selecionado:
        df_filtrado = df[df[coluna_filtro].isin(valor_selecionado)]
    else:
        df_filtrado = df  # Caso nenhum valor seja selecionado, mostra toda a tabela

# Exibir a tabela filtrada
st.write("### 🔎 Dados Filtrados")
st.dataframe(df_filtrado.drop(columns=[coluna_monetaria]).rename(columns={"RESP_RENDA_FORMATADA": "RESP_RENDA_MEDIA"}))

# Adicionar o filtro para selecionar o bairro (linha) para exibir no gráfico de pizza
st.write("## 📊 Gráfico de Pizza: Distribuição entre Homens e Mulheres")

# Criar filtro para selecionar o bairro (linha) para exibir no gráfico de pizza
bairro_selecionado = st.selectbox("Selecione o Bairro", df_filtrado["NOME_BAIRRO"].unique())

# Filtrar o DataFrame para mostrar os dados do bairro selecionado
df_bairro_selecionado = df_filtrado[df_filtrado["NOME_BAIRRO"] == bairro_selecionado]

# Selecionar apenas as colunas POP_TOTAL_HOMEM e POP_TOTAL_MULHER para o gráfico
valores_bairro = {
    "Homens": df_bairro_selecionado["POP_TOTAL_HOMEM"].iloc[0],
    "Mulheres": df_bairro_selecionado["POP_TOTAL_MULHER"].iloc[0]
}

# Criar gráfico de pizza com os valores do bairro selecionado
fig_pizza = px.pie(
    names=list(valores_bairro.keys()),  # Nomes: "Homens" e "Mulheres"
    values=list(valores_bairro.values()),  # Valores de POP_TOTAL_HOMEM e POP_TOTAL_MULHER
    title=f"Distribuição de Homens e Mulheres no Bairro: {bairro_selecionado}"
)
st.plotly_chart(fig_pizza)

# Mostrar o dado da coluna POP_TOTAL_RESIDENTE para o bairro selecionado
pop_total_residente = df_bairro_selecionado["POP_TOTAL_RESIDENTE"].iloc[0]
st.write(f"### População Total de Residentes no Bairro {bairro_selecionado}: {pop_total_residente}")

# Criar o gráfico de barras para as idades
st.write("## 📊 Gráfico de Barras: Distribuição por Faixa Etária")

# Selecionar os valores das faixas etárias
faixa_etaria = {
    "0-6 Anos": df_bairro_selecionado["IDADE_0_6_ANOS"].iloc[0],
    "7-14 Anos": df_bairro_selecionado["IDADE_7_14_ANOS"].iloc[0],
    "65+ Anos": df_bairro_selecionado["IDADE_65_MAIS"].iloc[0]
}

# Criar gráfico de barras com as faixas etárias
fig_barras = px.bar(
    x=list(faixa_etaria.keys()),  # Nomes das faixas etárias
    y=list(faixa_etaria.values()),  # Valores das faixas etárias
    title=f"Distribuição Etária no Bairro: {bairro_selecionado}",
    labels={'x': 'Faixa Etária', 'y': 'População'},
)

st.plotly_chart(fig_barras)

# Exibir o valor da variável GRAU_ENVELHECIMENTO para o bairro selecionado
grau_envelhecimento = df_bairro_selecionado["GRAU_ENVELHECIMENTO"].iloc[0]
st.write(f"### Grau de Envelhecimento no Bairro {bairro_selecionado}: {grau_envelhecimento}")

st.write("## 📊 Gráfico de Barras: População divida em COR por Bairro")

# Filtrar as colunas que contêm "COR_"
cor_cols = [col for col in df.columns if "COR_" in col]

# Verificar se existem colunas "COR_" no DataFrame
if cor_cols:
    # Selecionar os valores dessas colunas para o bairro selecionado
    cor_values = {col: df_bairro_selecionado[col].iloc[0] for col in cor_cols}

    # Criar gráfico de pizza com as variáveis "COR_"
    fig_cor = px.pie(
        names=list(cor_values.keys()),  # Nomes das cores
        values=list(cor_values.values()),  # Valores de cada cor
        title=f"Distribuição por Cor no Bairro: {bairro_selecionado}"
    )

    st.plotly_chart(fig_cor)
else:
    st.write("### Não há dados de cor disponíveis para o bairro selecionado.")

st.write("## 📊 Gráfico de Barras: Total de Domicilios, Lixo coletado, Saneamento adequado e Rede de agua por Bairro")

# Filtrar as colunas que contêm "DOM_"
dom_cols = [col for col in df.columns if "DOM_" in col]

# Verificar se existem colunas "DOM_" no DataFrame
if dom_cols:
    # Selecionar os valores dessas colunas para o bairro selecionado
    dom_values = {col: df_bairro_selecionado[col].iloc[0] for col in dom_cols}

    # Criar gráfico de barras com as variáveis "DOM_"
    fig_dom = px.bar(
        x=list(dom_values.keys()),  # Nomes das variáveis DOM_
        y=list(dom_values.values()),  # Valores das variáveis DOM_
        title=f"Dados dos Domicilios no Bairro: {bairro_selecionado}",
        labels={'x': 'Tipo de Domínio', 'y': 'Valor'},
    )

    st.plotly_chart(fig_dom)
else:
    st.write("### Não há dados de DOM disponíveis para o bairro selecionado.")

# Filtrar as colunas que contêm "PROP_"
prop_cols = [col for col in df.columns if "PROP_" in col]

# Verificar se existem colunas "PROP_" no DataFrame
if prop_cols:
    # Selecionar os valores dessas colunas para o bairro selecionado
    prop_values = {col: df_bairro_selecionado[col].iloc[0] for col in prop_cols}

    # Criar gráfico de colunas com as variáveis "PROP_"
    fig_prop = px.bar(
        x=list(prop_values.keys()),  # Nomes das variáveis PROP_
        y=list(prop_values.values()),  # Valores das variáveis PROP_
        title=f"Proporção entre Lixo Coletado, Seneamento adequado e Rede de agua por Domicilio: {bairro_selecionado}",
        labels={'x': 'Tipo de Proporção', 'y': 'Valor (%)'},
    )

    st.plotly_chart(fig_prop)
else:
    st.write("### Não há dados de PROP_ disponíveis para o bairro selecionado.")

# Exibir todos os dados da densidade populacional sem filtro
st.write("## 📊 Gráfico de Barras: Comparação da Densidade Populacional entre Todos os Bairros")

# Opções de ordenação para gráficos e tabela
st.write("### 🔽 Ordenação dos Dados")
opcoes_ordenacao = {
    "Nome do Bairro (A-Z)": ("NOME_BAIRRO", True),
    "Nome do Bairro (Z-A)": ("NOME_BAIRRO", False),
    "Densidade (Crescente)": ("DENSIDADE", True),
    "Densidade (Decrescente)": ("DENSIDADE", False),
}

criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

# Aplicar ordenação ao DataFrame antes de gerar gráficos
coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
df_filtrado = df_filtrado.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

# Criar gráfico de barras para comparar a DENSIDADE entre todos os bairros
fig_densidade = px.bar(
    df_filtrado,
    x="NOME_BAIRRO",  # Nome do Bairro
    y="DENSIDADE",  # Coluna de Densidade Populacional
    labels={'DENSIDADE': 'Densidade Populacional', 'NOME_BAIRRO': 'Bairro'},
)

st.plotly_chart(fig_densidade)

# Novo gráfico para RESP_RENDA_MEDIA
st.write("## 📊 Tabela: Média de Renda entre Bairros")

# Opções de ordenação para gráficos e tabela
st.write("### 🔽 Ordenação dos Dados")
opcoes_ordenacao = {
    "Nome do Bairro (A-Z)": ("NOME_BAIRRO", True),
    "Nome do Bairro (Z-A)": ("NOME_BAIRRO", False),
    "Renda Média (Crescente)": ("RESP_RENDA_MEDIA", True),
    "Renda Média (Decrescente)": ("RESP_RENDA_MEDIA", False),
}

criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

# Aplicar ordenação ao DataFrame antes de gerar gráficos
coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
df_filtrado = df_filtrado.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

# Criar gráfico de barras corrigido
fig_renda = px.bar(
    df_filtrado,
    x="NOME_BAIRRO",  # Nome do Bairro
    y="RESP_RENDA_MEDIA",  # Coluna de Média de Renda (agora numérica)
    labels={'RESP_RENDA_MEDIA': 'Média de Renda (R$)', 'NOME_BAIRRO': 'Bairro'},
)

st.plotly_chart(fig_renda)

#Titulo do grafico de Analfaabetismo
st.write("## 📊 Gráfico de Barras: Taxa de Analfabetismo por Bairro")

# Opções de ordenação para gráficos e tabela
st.write("### 🔽 Ordenação dos Dados")
opcoes_ordenacao = {
    "Nome do Bairro (A-Z)": ("NOME_BAIRRO", True),
    "Nome do Bairro (Z-A)": ("NOME_BAIRRO", False),
    "Educação Analfabeta (Crescente)": ("EDUC_ANALFABETISMO", True),
    "Educação Analfabeta (Decrescente)": ("EDUC_ANALFABETISMO", False),
}

criterio_ordenacao = st.selectbox("Escolha o critério de ordenação", list(opcoes_ordenacao.keys()))

# Aplicar ordenação ao DataFrame antes de gerar gráficos
coluna_ordenacao, ordem_crescente = opcoes_ordenacao[criterio_ordenacao]
df_filtrado = df_filtrado.sort_values(by=coluna_ordenacao, ascending=ordem_crescente)

# Adicionar gráfico de barras para a taxa de analfabetismo
if "EDUC_ANALFABETISMO" in df.columns:
    fig_analfabetismo = px.bar(
        df_filtrado,
        x="NOME_BAIRRO",
        y="EDUC_ANALFABETISMO",
        labels={'EDUC_ANALFABETISMO': 'Taxa de Analfabetismo (%)', 'NOME_BAIRRO': 'Bairro'},
    )
    st.plotly_chart(fig_analfabetismo)
else:
    st.write("### Não há dados de analfabetismo disponíveis na planilha.")
