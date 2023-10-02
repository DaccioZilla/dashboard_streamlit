import plotly.express as px

def mapa_receita_por_estado(receita_por_estado):
    g_receita_por_estado = px.scatter_geo(receita_por_estado, 
                                            lat = 'lat', 
                                            lon = 'lon', 
                                            size= 'Preço', 
                                            template= 'seaborn', 
                                            scope = 'world',
                                            hover_name= 'Local da compra',
                                            hover_data = {'lat': False, 'lon': False},
                                            title= 'Receita por estado'
                                            )
        
    g_receita_por_estado.update_geos(fitbounds="locations", showcountries = True)
    g_receita_por_estado.update_layout(
        margin=dict(l=0, r=0, t=20, b=0)
    )

    return g_receita_por_estado

def barra_receita_por_estado(receita_por_estado):
    bar_receita_por_estado = px.bar(
        receita_por_estado.head(),
        x = 'Local da compra',
        y = 'Preço',
        text_auto= True,
        title= 'Top Estados (Receita)'
    )
    bar_receita_por_estado.update_layout(yaxis_title = 'Receita')
    return bar_receita_por_estado

def barra_receita_por_categoria(receita_por_categoria):
    bar_receita_por_categoria = px.bar(
        receita_por_categoria,
        x = 'Categoria do Produto',
        y = 'Preço',
        text_auto= True,
        title= 'Top Categorias (Receita)'
    )
    bar_receita_por_categoria.update_layout(yaxis_title = 'Receita')
    return bar_receita_por_categoria

def linha_receita_mensal(receita_mensal):
    g_receita_mensal = px.line(receita_mensal,
                           x = 'Mes',
                           y = 'Preço',
                           markers= True,
                           range_y= (0,receita_mensal.max()),
                           color = 'Ano',
                           line_dash = "Ano",
                           title= 'Receita Mensal'
                           )

    g_receita_mensal.update_layout(yaxis_title = 'Receita')
    return g_receita_mensal

def barra_receita_por_vendedores(vendedores, qtd_vendedores):
    receita_vendedores = px.bar(vendedores.sort_values('sum', ascending= False).head(qtd_vendedores),
                                        x = 'sum',
                                        y = 'Vendedor',
                                        text_auto= True,
                                        title= f'Top {qtd_vendedores} Vendedores (Receita)'
                                        )
    return receita_vendedores

def barra_quantidade_vendas_por_vendedores(vendedores, qtd_vendedores):
    receita_vendedores = px.bar(vendedores.sort_values('count', ascending= False).head(qtd_vendedores),
                                        x = 'count',
                                        y = 'Vendedor',
                                        text_auto= True,
                                        title= f'Top {qtd_vendedores} Vendedores (Receita)'
                                        )
    return receita_vendedores

def mapa_quantidade_de_vendas_por_estado(vendas_por_estado):
    g_receita_por_estado = px.scatter_geo(vendas_por_estado, 
                                            lat = 'lat', 
                                            lon = 'lon', 
                                            size= 'qtd_vendas', 
                                            template= 'seaborn', 
                                            scope = 'world',
                                            hover_name= 'Local da compra',
                                            hover_data = {'lat': False, 'lon': False},
                                            title= 'Vendas por estado'
                                            )
        
    g_receita_por_estado.update_geos(fitbounds="locations", showcountries = True)
    g_receita_por_estado.update_layout(
        margin=dict(l=0, r=0, t=20, b=0)
    )
    return g_receita_por_estado

def linha_vendas_mensais(vendas_mensais):
    g_vendas_mensais = px.line(vendas_mensais,
                           x = 'Mes',
                           y = 'qtd_vendas',
                           markers= True,
                           range_y= (0,vendas_mensais.max()),
                           color = 'Ano',
                           line_dash = "Ano",
                           title= 'Vendas Mensais'
                           )

    g_vendas_mensais.update_layout(yaxis_title = 'Qtd Vendas')
    return g_vendas_mensais

def barra_vendas_por_categoria(vendas_por_categoria):
    bar_receita_por_categoria = px.bar(
        vendas_por_categoria,
        x = 'Categoria do Produto',
        y = 'qtd_vendas',
        text_auto= True,
        title= 'Top Categorias (Qtd de Vendas)'
    )
    bar_receita_por_categoria.update_layout(yaxis_title = 'Qtd Vendas')
    return bar_receita_por_categoria

def barra_vendas_por_estado(vendas_por_estado):
    bar_vendas_por_estado = px.bar(
        vendas_por_estado.head(),
        x = 'Local da compra',
        y = 'qtd_vendas',
        text_auto= True,
        title= 'Top Estados (Qtd de Vendas)'
    )
    bar_vendas_por_estado.update_layout(yaxis_title = 'Qtd de Vendas')
    return bar_vendas_por_estado

if __name__ == '__main__':
    pass