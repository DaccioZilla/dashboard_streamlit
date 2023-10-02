import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from plots import (mapa_receita_por_estado, barra_receita_por_estado, barra_receita_por_categoria, linha_receita_mensal, 
                   barra_quantidade_vendas_por_vendedores, barra_receita_por_vendedores, mapa_quantidade_de_vendas_por_estado,
                   linha_vendas_mensais, barra_vendas_por_categoria, barra_vendas_por_estado)

st.set_page_config(layout= 'wide')

def number_formatter(valor, prefix = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefix} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefix} {valor:.2f} milhões'

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

### Consumo dos Dados Iniciais
url = 'https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)
regiao = '' if regiao == 'Brasil' else regiao

todos_anos = st.sidebar.checkbox('Dados de todos os anos', value= True)
ano = '' if todos_anos else st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao': regiao.lower(), 'ano': ano}

response = requests.get(url, params= query_string)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')
filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]

### Tabelas de Receita
receita_por_estado = dados.groupby(['Local da compra', 'lat', 'lon'])['Preço'].sum().reset_index().sort_values('Preço', ascending= False)
receita_por_categoria = dados.groupby(['Categoria do Produto'])['Preço'].sum().reset_index().sort_values('Preço', ascending= False)
receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq= 'M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month

### Plots Receita
g_receita_por_estado = mapa_receita_por_estado(receita_por_estado)  
bar_receita_por_estado = barra_receita_por_estado(receita_por_estado)
bar_receita_por_categoria = barra_receita_por_categoria(receita_por_categoria)
g_receita_mensal = linha_receita_mensal(receita_mensal)

### Tabelas de Quantidade de Vendas
vendas_por_estado = dados.groupby(['Local da compra', 'lat', 'lon']).agg(qtd_vendas = ('Preço', 'count')).reset_index().sort_values('qtd_vendas', ascending= False)
vendas_mensais = dados.set_index('Data da Compra').groupby(pd.Grouper(freq= 'M')).agg(qtd_vendas = ('Preço', 'count')).reset_index()
vendas_mensais['Ano'] = vendas_mensais['Data da Compra'].dt.year
vendas_mensais['Mes'] = vendas_mensais['Data da Compra'].dt.month
vendas_mensais['Mes'] = vendas_mensais['Data da Compra'].dt.month
vendas_por_categoria = dados.groupby(['Categoria do Produto']).agg(qtd_vendas = ('Preço', 'count')).reset_index().sort_values('qtd_vendas', ascending= False)

### Plots Quantidade de Vendas
map_vendas_por_estado = mapa_quantidade_de_vendas_por_estado(vendas_por_estado)
fig_vendas_mensais = linha_vendas_mensais(vendas_mensais)
fig_vendas_por_categoria = barra_vendas_por_categoria(vendas_por_categoria)
fig_vendas_por_estado = barra_vendas_por_estado(vendas_por_estado)

### Tabelas de Vendedores
vendedores = dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']).reset_index()

### Estrutura do Dashboard
aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de vendas', 'Vendedores'])

with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Receita', number_formatter(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(g_receita_por_estado, use_container_width= True)
    with col2:
        st.metric('Quantidade de Vendas', number_formatter(dados['Preço'].count()))
        st.plotly_chart(g_receita_mensal, use_container_width= True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bar_receita_por_categoria, use_container_width= True)
    with col2:
        st.plotly_chart(bar_receita_por_estado, use_container_width= True)
with aba2:
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Receita', number_formatter(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(map_vendas_por_estado, use_container_width= True)

    with col2:
        st.metric('Quantidade de Vendas', number_formatter(dados['Preço'].count()))
        st.plotly_chart(fig_vendas_mensais, use_container_width= True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_vendas_por_categoria, use_container_width= True)
    with col2:
        st.plotly_chart(fig_vendas_por_estado, use_container_width= True)

with aba3:
    qtd_vendedores = st.number_input('Quantidade de Vendedores', min_value= 2, max_value= 10, value= 5) 
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Receita', number_formatter(dados['Preço'].sum(), 'R$'))
        receita_vendedores = barra_receita_por_vendedores(vendedores, qtd_vendedores)
        st.plotly_chart(receita_vendedores, use_container_width= True)

    with col2:
        st.metric('Quantidade de Vendas', number_formatter(dados['Preço'].count()))
        vendas_vendedores = barra_quantidade_vendas_por_vendedores(vendedores, qtd_vendedores)
        st.plotly_chart(vendas_vendedores, use_container_width= True)

