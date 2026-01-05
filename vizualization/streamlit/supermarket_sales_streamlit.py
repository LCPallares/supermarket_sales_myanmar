import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas de Supermercado de Myanmar", layout="wide")

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("supermarket_Sales.csv")
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
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    return df

df = cargar_datos()

# Coordenadas de las ciudades de Myanmar
city_coordinates = {
    'Yangon': [16.8409, 96.1735],
    'Naypyitaw': [19.7633, 96.0785],
    'Mandalay': [21.9588, 96.0891]  # Agregamos Mandalay por si acaso
}

# Funciones para los gráficos
def graficar_ventas_diarias(df):
    ventas_diarias = df.groupby('Fecha')['Total'].sum().reset_index()
    fig = px.line(ventas_diarias, x='Fecha', y='Total', title='Ventas Diarias')
    st.plotly_chart(fig, use_container_width=True)

def graficar_ventas_por_tipo_cliente_y_genero(df):
    ventas_tipo_genero = df.groupby(['Tipo de Cliente', 'Género'])['Total'].sum().unstack()
    fig = px.bar(ventas_tipo_genero, title='Ventas por Tipo de Cliente y Género', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def graficar_ventas_por_linea_de_producto(df):
    productos = df['Línea de Producto'].value_counts()
    fig = px.pie(values=productos.values, names=productos.index, title='Ventas por Línea de Producto')
    st.plotly_chart(fig, use_container_width=True)

def graficar_mapa_de_ventas(df):
    m = folium.Map(location=[19.7500, 96.0800], zoom_start=6)  # Centrado en Myanmar
    for city, sales in df.groupby('Ciudad')['Total'].sum().items():
        if city in city_coordinates:
            folium.Marker(
                location=city_coordinates[city],
                popup=f"{city}: ${sales:,.2f}",
                icon=folium.Icon(color='red', icon='dollar-sign', prefix='fa')
            ).add_to(m)
    st_folium(m, width=800, height=500)

def graficar_metodos_de_pago(df):
    metodos_pago = df['Método de Pago'].value_counts()
    fig = px.pie(values=metodos_pago.values, names=metodos_pago.index, title='Métodos de Pago')
    st.plotly_chart(fig, use_container_width=True)

def graficar_cantidad_de_productos(df):
    ventas_cantidad = df.groupby('Línea de Producto')['Cantidad'].sum().sort_values(ascending=False)
    fig = px.bar(ventas_cantidad, title='Cantidad de Productos Vendidos por Línea de Producto')
    st.plotly_chart(fig, use_container_width=True)

def graficar_distribucion_precios_unitarios(df):
    fig = px.histogram(df, x="Precio Unitario", nbins=20, title="Distribución de Precios Unitarios")
    st.plotly_chart(fig, use_container_width=True)

def mostrar_metricas(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ventas Totales", f"${df['Total'].sum():,.2f}")
    col2.metric("Transacciones", f"{len(df):,}")
    col3.metric("Venta Promedio", f"${df['Total'].mean():,.2f}")
    col4.metric("Margen Bruto Promedio", f"${df['Ingreso Bruto'].mean():,.2f}")

def mostrar_analisis_margen_bruto(df):
    st.subheader("Análisis del Margen Bruto")
    margen_promedio = df['Porcentaje de Margen Bruto'].mean()
    st.write(f"El margen bruto promedio es: {margen_promedio:.2f}%")

# Título y barra de navegación
st.title("Dashboard de Ventas de Supermercado de Myanmar")
nav = st.sidebar.radio("Navegar a", ["Métricas", "Gráficos", "Tabla de Datos"])

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    start_date = st.date_input("Fecha de inicio", df['Fecha'].min())
with col2:
    end_date = st.date_input("Fecha de fin", df['Fecha'].max())
with col3:
    ciudades = st.multiselect("Seleccionar ciudades", df['Ciudad'].unique())
    productos = st.multiselect("Seleccionar líneas de producto", df['Línea de Producto'].unique())

# Aplicar filtros
mask = (df['Fecha'].dt.date >= start_date) & (df['Fecha'].dt.date <= end_date)
if ciudades:
    mask &= df['Ciudad'].isin(ciudades)
if productos:
    mask &= df['Línea de Producto'].isin(productos)
filtered_df = df[mask]

# Mostrar la sección seleccionada en la barra de navegación
if nav == "Métricas":
    mostrar_metricas(filtered_df)
    #graficar_metodos_de_pago(filtered_df)

elif nav == "Gráficos":
    col1, col2 = st.columns(2)

    with col1:
        graficar_ventas_diarias(filtered_df)
        graficar_ventas_por_tipo_cliente_y_genero(filtered_df)

    with col2:
        graficar_ventas_por_linea_de_producto(filtered_df)
        graficar_mapa_de_ventas(filtered_df)
    
    graficar_metodos_de_pago(filtered_df)

    graficar_cantidad_de_productos(filtered_df)
    graficar_distribucion_precios_unitarios(filtered_df)

elif nav == "Tabla de Datos":
    st.dataframe(filtered_df)
    #graficar_metodos_de_pago(filtered_df)

# Añadir más componentes
st.markdown("---")

#graficar_cantidad_de_productos(filtered_df)
#graficar_distribucion_precios_unitarios(filtered_df)
#mostrar_analisis_margen_bruto(filtered_df)