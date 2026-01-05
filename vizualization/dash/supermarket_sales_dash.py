# Importación de librerías necesarias
import dash
from dash import html, dcc, Input, Output  # Componentes de Dash
import dash_bootstrap_components as dbc  # Para estilos
import pandas as pd  # Para manipulación de datos
import plotly.express as px  # Para crear gráficos
import plotly.graph_objects as go  # Para gráficos más personalizados

# Cargar datos desde la URL
data_url = "https://raw.githubusercontent.com/plotly/datasets/master/supermarket_Sales.csv"
df = pd.read_csv(data_url)
# Cargar datos local
# datos = "supermarket_Sales.csv"
# df = pd.read_csv(datos)

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

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Componentes de filtro
filtro_fecha = dcc.DatePickerRange(
    id='filtro-fecha',
    start_date=df['Fecha'].min(),
    end_date=df['Fecha'].max(),
    display_format='YYYY-MM-DD'
)

filtro_ciudad = dcc.Dropdown(
    id='filtro-ciudad',
    options=[{'label': ciudad, 'value': ciudad} for ciudad in df['Ciudad'].unique()],
    multi=True,
    placeholder="Seleccionar ciudad(es)"
)

filtro_producto = dcc.Dropdown(
    id='filtro-producto',
    options=[{'label': producto, 'value': producto} for producto in df['Línea de Producto'].unique()],
    multi=True,
    placeholder="Seleccionar línea(s) de producto"
)

# Definir estilos personalizados
styles = {
    'background': '#EAEDF2FF',
    'filters_row': {'backgroundColor': '#333333FF', 'padding': '20px', 'borderRadius': '10px', 'margin-bottom': '20px'},
    'metrics_row': {'backgroundColor': '#45474DFF', 'padding': '20px', 'borderRadius': '10px', 'margin-bottom': '20px'},
    'card_ventas_totales': {'backgroundColor': '#96E0B2FF'},
    'card_transacciones': {'backgroundColor': '#C1E7FCFF'},
    'card_venta_promedio': {'backgroundColor': '#F6B6EAFF'},
    'card_margen_bruto': {'backgroundColor': '#C1E7FCFF'},
}

# Definir el layout de la aplicación con los nuevos estilos
app.layout = dbc.Container([
    html.H1("Dashboard de Ventas de Supermercado", className="my-4", style={'textAlign': 'center'}),
    
    # Fila de filtros
    dbc.Row([
        dbc.Col(filtro_fecha, width=4),
        dbc.Col(filtro_ciudad, width=4),
        dbc.Col(filtro_producto, width=4),
    ], style=styles['filters_row']),
    
    # Fila de métricas principales
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Ventas Totales"), html.H2(id="ventas-totales")]), style=styles['card_ventas_totales']), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Transacciones"), html.H2(id="num-transacciones")]), style=styles['card_transacciones']), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Venta Promedio"), html.H2(id="venta-promedio")]), style=styles['card_venta_promedio']), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Margen Bruto Promedio"), html.H2(id="margen-bruto-promedio")]), style=styles['card_margen_bruto']), width=3),
    ], style=styles['metrics_row']),
    
    # Fila de gráficos: ventas diarias y productos
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-ventas-diarias'), width=8),
        dbc.Col(dcc.Graph(id='grafico-productos'), width=4),
    ], className="mb-4"),
    
    # Fila de gráficos: tipo de cliente/género y ventas por ciudad
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-tipo-genero'), width=8),
        dbc.Col(dcc.Graph(id='grafico-ciudad'), width=4),
    ], className="mb-4"),
    
    # Fila de gráfico: métodos de pago
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-metodos-pago'), width=12),
    ])
], style={'backgroundColor': styles['background'], 'padding': '20px'})  # Aplicar color de fondo al contenedor principal

# El callback y la función update_dashboard permanecen sin cambios
@app.callback(
    [Output('ventas-totales', 'children'),
     Output('num-transacciones', 'children'),
     Output('venta-promedio', 'children'),
     Output('margen-bruto-promedio', 'children'),
     Output('grafico-ventas-diarias', 'figure'),
     Output('grafico-productos', 'figure'),
     Output('grafico-tipo-genero', 'figure'),
     Output('grafico-ciudad', 'figure'),
     Output('grafico-metodos-pago', 'figure')],
    [Input('filtro-fecha', 'start_date'),
     Input('filtro-fecha', 'end_date'),
     Input('filtro-ciudad', 'value'),
     Input('filtro-producto', 'value')]
)
def update_dashboard(start_date, end_date, ciudades, productos):
    dff = df.copy()
    
    if start_date and end_date:
        dff = dff[(dff['Fecha'] >= start_date) & (dff['Fecha'] <= end_date)]
    
    if ciudades:
        dff = dff[dff['Ciudad'].isin(ciudades)]
    
    if productos:
        dff = dff[dff['Línea de Producto'].isin(productos)]
    
    ventas_totales = dff['Total'].sum()
    num_transacciones = len(dff)
    venta_promedio = ventas_totales / num_transacciones if num_transacciones > 0 else 0
    margen_bruto_promedio = dff['Ingreso Bruto'].mean()

    ventas_diarias = dff.groupby('Fecha')['Total'].sum().reset_index()
    fig_ventas_diarias = px.line(ventas_diarias, x='Fecha', y='Total', title='Ventas Diarias')

    productos = dff['Línea de Producto'].value_counts()
    fig_productos = px.pie(values=productos.values, names=productos.index, title='Ventas por Línea de Producto')

    ventas_tipo_genero = dff.groupby(['Tipo de Cliente', 'Género'])['Total'].sum().unstack()
    fig_tipo_genero = px.bar(ventas_tipo_genero, title='Ventas por Tipo de Cliente y Género', barmode='group')

    ventas_ciudad = dff.groupby('Ciudad')['Total'].sum().sort_values(ascending=True)
    fig_ciudad = px.bar(ventas_ciudad, orientation='h', title='Ventas por Ciudad')

    metodos_pago = dff['Método de Pago'].value_counts()
    fig_metodos_pago = px.pie(values=metodos_pago.values, names=metodos_pago.index, title='Métodos de Pago')

    return (
        f"${ventas_totales:,.2f}",
        f"{num_transacciones}",
        f"${venta_promedio:,.2f}",
        f"${margen_bruto_promedio:,.2f}",
        fig_ventas_diarias,
        fig_productos,
        fig_tipo_genero,
        fig_ciudad,
        fig_metodos_pago
    )

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)