import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar datos (asumimos que tienes un CSV similar)
# df = pd.read_csv("datos_ventas.csv")
# Cargar datos desde el archivo CSV
datos = "supermarket_Sales.csv"
df = pd.read_csv(datos)

# Diccionario para traducir nombres de columnas
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

# Renombrar las columnas del DataFrame
df = df.rename(columns=columnas_traducidas)


df['Fecha'] = pd.to_datetime(df['Fecha'])

# Calcular métricas
ventas_totales = df['Monto'].sum()
oportunidades = len(df)
tamano_promedio = ventas_totales / oportunidades
velocidad_promedio = df['Dias_Ciclo'].mean()

# Gráfico de ventas y oportunidades por mes
ventas_mensuales = df.groupby(df['Fecha'].dt.strftime('%b'))['Monto'].sum().reset_index()
oportunidades_mensuales = df.groupby(df['Fecha'].dt.strftime('%b'))['ID'].count().reset_index()

fig_mensual = go.Figure()
fig_mensual.add_trace(go.Scatter(x=ventas_mensuales['Fecha'], y=ventas_mensuales['Monto'], name='Ventas', line=dict(color='royalblue')))
fig_mensual.add_trace(go.Scatter(x=oportunidades_mensuales['Fecha'], y=oportunidades_mensuales['ID'], name='Oportunidades', line=dict(color='turquoise')))
fig_mensual.update_layout(title='Ventas y Oportunidades por Mes', xaxis_title='Mes', yaxis_title='Cantidad')

# Gráfico de canales de marketing
canales = df['Canal'].value_counts()
fig_canales = px.pie(values=canales.values, names=canales.index, title='Ventas por Canales de Marketing')

# Gráfico de etapas de venta por canal
etapas_canal = df.groupby(['Etapa', 'Canal'])['Monto'].sum().unstack()
fig_etapas = px.bar(etapas_canal, title='Etapas de Venta por Canal', barmode='group')

# Gráfico de oportunidades por tamaño
bins = [0, 20000, 40000, 60000, float('inf')]
labels = ['20K o menos', '20K a 40K', '40K a 60K', 'Más de 60K']
df['Rango_Tamano'] = pd.cut(df['Monto'], bins=bins, labels=labels, include_lowest=True)
tamanos = df['Rango_Tamano'].value_counts().sort_index()
fig_tamanos = px.bar(x=tamanos.index, y=tamanos.values, title='Oportunidades por Tamaño')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dashboard de Ventas", className="my-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Ventas"), html.H2(f"${ventas_totales:,.0f}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Oportunidades"), html.H2(f"{oportunidades}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Tamaño Promedio"), html.H2(f"${tamano_promedio:,.0f}")])], color="light")),
        dbc.Col(dbc.Card([dbc.CardBody([html.H4("Velocidad Promedio"), html.H2(f"{velocidad_promedio:.2f}")])], color="light")),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_mensual), width=8),
        dbc.Col(dcc.Graph(figure=fig_canales), width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_etapas), width=8),
        dbc.Col(dcc.Graph(figure=fig_tamanos), width=4),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
