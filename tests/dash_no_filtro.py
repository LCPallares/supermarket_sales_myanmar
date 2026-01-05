import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos desde la URL
data_url = "https://raw.githubusercontent.com/plotly/datasets/master/supermarket_Sales.csv"
df = pd.read_csv(data_url)
print(df.columns)
df['Date'] = pd.to_datetime(df['Date'])

# Calcular métricas
ventas_totales = df['Total'].sum()
num_transacciones = len(df)
tamano_promedio = ventas_totales / num_transacciones
margen_bruto_promedio = df['Gross income'].mean()

# Gráfico de ventas y cantidad por mes
ventas_mensuales = df.groupby(df['Date'].dt.strftime('%b'))['Total'].sum().reset_index()
cantidad_mensuales = df.groupby(df['Date'].dt.strftime('%b'))['Quantity'].sum().reset_index()

fig_mensual = go.Figure()
fig_mensual.add_trace(go.Scatter(x=ventas_mensuales['Date'], y=ventas_mensuales['Total'], name='Ventas', line=dict(color='royalblue')))
fig_mensual.add_trace(go.Scatter(x=cantidad_mensuales['Date'], y=cantidad_mensuales['Quantity'], name='Cantidad', line=dict(color='turquoise')))
fig_mensual.update_layout(title='Ventas y Cantidad por Mes', xaxis_title='Mes', yaxis_title='Valor')

# Gráfico de líneas de productos
productos = df['Product line'].value_counts()
fig_productos = px.pie(values=productos.values, names=productos.index, title='Ventas por Línea de Producto')

# Gráfico de ventas por tipo de cliente y línea de producto
ventas_tipo_producto = df.groupby(['Customer type', 'Product line'])['Total'].sum().unstack()
fig_tipo_producto = px.bar(ventas_tipo_producto, title='Ventas por Tipo de Cliente y Línea de Producto', barmode='group')

# Gráfico de ventas por ciudad
ventas_ciudad = df.groupby('City')['Total'].sum().sort_values(ascending=True)
fig_ciudad = px.bar(ventas_ciudad, orientation='h', title='Ventas por Ciudad')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dashboard de Ventas de Supermercado", className="my-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Ventas Totales"), html.H2(f"${ventas_totales:,.2f}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Transacciones"), html.H2(f"{num_transacciones}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Venta Promedio"), html.H2(f"${tamano_promedio:,.2f}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Margen Bruto Promedio"), html.H2(f"${margen_bruto_promedio:,.2f}")])], color="light")),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_mensual), width=8),
        dbc.Col(dcc.Graph(figure=fig_productos), width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_tipo_producto), width=8),
        dbc.Col(dcc.Graph(figure=fig_ciudad), width=4),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
