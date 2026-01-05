import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos desde la URL
data_url = "https://raw.githubusercontent.com/plotly/datasets/master/supermarket_Sales.csv"
df = pd.read_csv(data_url)
# Cargar datos local
# datos = "supermarket_Sales.csv"
# df = pd.read_csv(datos)

columnas_traducidas = {
    'Invoice ID': 'ID de Factura',
    'Branch': 'Sucursal',
    'City': 'Ciudad',
    'Customer type': 'Tipo de Cliente',
    'Gender': 'Género',
    'Product line': 'Línea de Producto',
    'Unit price': 'Precio Unitario',
    'Quantity': 'Cantidad',
    'Tax 5%': 'Impuesto 5%',
    'Total': 'Total',
    'Date': 'Fecha',
    'Time': 'Hora',
    'Payment': 'Método de Pago',
    'Cost of goods sold': 'Costo de Bienes Vendidos',
    'Gross margin percentage': 'Porcentaje de Margen Bruto',
    'Gross income': 'Ingreso Bruto',
    'Customer stratification rating': 'Calificación de Estratificación del Cliente'
}

df = df.rename(columns=columnas_traducidas)

# Convertir la columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Calcular métricas
ventas_totales = df['Total'].sum()
num_transacciones = len(df)
venta_promedio = ventas_totales / num_transacciones
margen_bruto_promedio = df['Ingreso Bruto'].mean()

#print(f"\nventas_totales: {ventas_totales}\n \nnum_transacciones: {num_transacciones}\n \nventa_promedio: {venta_promedio}\n \nmargen_bruto_promedio: {margen_bruto_promedio}\n")


# Gráfico de ventas diarias
ventas_diarias = df.groupby('Fecha')['Total'].sum().reset_index()
fig_ventas_diarias = px.line(ventas_diarias, x='Fecha', y='Total', title='Ventas Diarias')

# Gráfico de líneas de productos
productos = df['Línea de Producto'].value_counts()
fig_productos = px.pie(values=productos.values, names=productos.index, title='Ventas por Línea de Producto')

# Gráfico de ventas por tipo de cliente y género
ventas_tipo_genero = df.groupby(['Tipo de Cliente', 'Género'])['Total'].sum().unstack()
fig_tipo_genero = px.bar(ventas_tipo_genero, title='Ventas por Tipo de Cliente y Género', barmode='group')

# Gráfico de ventas por ciudad
ventas_ciudad = df.groupby('Ciudad')['Total'].sum().sort_values(ascending=True)
fig_ciudad = px.bar(ventas_ciudad, orientation='h', title='Ventas por Ciudad')

# Gráfico de métodos de pago
metodos_pago = df['Método de Pago'].value_counts()
fig_metodos_pago = px.pie(values=metodos_pago.values, names=metodos_pago.index, title='Métodos de Pago')

"""
fig_ventas_diarias.show()
fig_productos.show()
fig_tipo_genero.show()
fig_ciudad.show()
fig_metodos_pago.show()
"""

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#09b39d
app.layout = dbc.Container([
    html.H1("Dashboard de Ventas de Supermercado", className="my-4"),
    
    dbc.Row([ # hex f6f8fb rgb 246, 248, 251
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Ventas Totales"),
                                        html.H2(f"${ventas_totales:,.2f}")])
                                ], style={'background-color': '#09b39d', 'color': 'green'}
                    ), style={'background-color': '#e7f4f6'}),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Transacciones"), html.H2(f"{num_transacciones}")])], color="light", style={'background-color': 'hex(f1963a)', 'color': 'blue'})),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Venta Promedio"), html.H2(f"${venta_promedio:,.2f}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Margen Bruto Promedio"), html.H2(f"${margen_bruto_promedio:,.2f}")])], color="light")),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_ventas_diarias), width=8),
        dbc.Col(dcc.Graph(figure=fig_productos), width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_tipo_genero), width=8),
        dbc.Col(dcc.Graph(figure=fig_ciudad), width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_metodos_pago), width=12),
    ])
])

if __name__ == '__main__':
    app.run(debug=True)

