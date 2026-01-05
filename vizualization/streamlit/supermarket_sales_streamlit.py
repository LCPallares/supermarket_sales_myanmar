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
    # para poner las metricas verticales remplazar col(n) por st
    col1.metric("Ventas Totales", f"${df['Total'].sum():,.2f}")
    col2.metric("Transacciones", f"{len(df):,}")
    col3.metric("Venta Promedio", f"${df['Total'].mean():,.2f}")
    col4.metric("Margen Bruto Promedio", f"${df['Ingreso Bruto'].mean():,.2f}")

def mostrar_analisis_margen_bruto(df):
    st.subheader("Análisis del Margen Bruto")
    margen_promedio = df['Porcentaje de Margen Bruto'].mean()
    st.write(f"El margen bruto promedio es: {margen_promedio:.2f}%")

def mostrar_top_productos(filtered_df):
    # Calcular top productos
    top_products = filtered_df.groupby('Línea de Producto')['Cantidad'].sum().reset_index()
    top_products = top_products.sort_values(by='Cantidad', ascending=False).head(5)
    top_products.columns = ['producto', 'cantidad']
    
    # Convertir los datos a tipos nativos de Python
    top_products['cantidad'] = top_products['cantidad'].astype(int).tolist()
    
    # Crear el dataframe con la configuración actualizada
    st.dataframe(
        top_products,
        column_order=("producto", "cantidad"),
        hide_index=True,
        width=None,
        column_config={
            "producto": st.column_config.TextColumn(
                "Producto",
            ),
            "cantidad": st.column_config.ProgressColumn(
                "Cantidad",
                format="%d",
                min_value=0,
                max_value=int(max(top_products['cantidad'])),
            )}
    )

# Título y barra de navegación
st.sidebar.header("Secciones")
st.title("Dashboard de Ventas de Supermercado de Myanmar")
nav = st.sidebar.radio("Navegar a", ["Ventas", "Tabla de Datos"])

# Filtros en el sidebar
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Fecha de inicio", df['Fecha'].min())
end_date = st.sidebar.date_input("Fecha de fin", df['Fecha'].max())
ciudades = st.sidebar.multiselect("Seleccionar ciudades", df['Ciudad'].unique())
productos = st.sidebar.multiselect("Seleccionar líneas de producto", df['Línea de Producto'].unique())

# Aplicar filtros
mask = (df['Fecha'].dt.date >= start_date) & (df['Fecha'].dt.date <= end_date)
if ciudades:
    mask &= df['Ciudad'].isin(ciudades)
if productos:
    mask &= df['Línea de Producto'].isin(productos)
filtered_df = df[mask]

# Sección de ventas
if nav == "Ventas":
    mostrar_metricas(filtered_df)
    graficar_mapa_de_ventas(filtered_df)
    col1, col2, col3 = st.columns((1.5, 4.5, 2), gap='medium')  # margenes de las columnas
    
    with col1:
        graficar_ventas_diarias(filtered_df)
        graficar_ventas_por_tipo_cliente_y_genero(filtered_df)
        graficar_cantidad_de_productos(filtered_df)

    with col2:
        graficar_ventas_por_linea_de_producto(filtered_df)
        graficar_metodos_de_pago(filtered_df)
        graficar_distribucion_precios_unitarios(filtered_df)

    with col3:
        st.markdown('#### Top Productos')
        mostrar_top_productos(filtered_df)
        
        with st.expander('Acerca de', expanded=True):
            st.write('''
                - Datos: [Datos de ventas de supermercado en Myanmar](ficticio-data-source.com).
                - :orange[**Top Productos**]: productos más vendidos por cantidad para el periodo seleccionado.
                - :orange[**Cantidad**]: número de unidades vendidas.
                ''')

    mostrar_analisis_margen_bruto(filtered_df)

elif nav == "Tabla de Datos":
    st.dataframe(filtered_df)

# Añadir más componentes
st.markdown("---")
