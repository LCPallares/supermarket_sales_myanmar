import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas de Supermercado", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
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

df = load_data()

# Título y barra de navegación
st.title("Dashboard de Ventas de Supermercado")
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
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ventas Totales", f"${filtered_df['Total'].sum():,.2f}")
    col2.metric("Transacciones", f"{len(filtered_df):,}")
    col3.metric("Venta Promedio", f"${filtered_df['Total'].mean():,.2f}")
    col4.metric("Margen Bruto Promedio", f"${filtered_df['Ingreso Bruto'].mean():,.2f}")

elif nav == "Gráficos":
    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Ventas Diarias
        ventas_diarias = filtered_df.groupby('Fecha')['Total'].sum().reset_index()
        fig_ventas_diarias = px.line(ventas_diarias, x='Fecha', y='Total', title='Ventas Diarias')
        st.plotly_chart(fig_ventas_diarias, use_container_width=True)

        # Ventas por Tipo de Cliente y Género
        ventas_tipo_genero = filtered_df.groupby(['Tipo de Cliente', 'Género'])['Total'].sum().unstack()
        fig_tipo_genero = px.bar(ventas_tipo_genero, title='Ventas por Tipo de Cliente y Género', barmode='group')
        st.plotly_chart(fig_tipo_genero, use_container_width=True)

    with col2:
        # Ventas por Línea de Producto
        productos = filtered_df['Línea de Producto'].value_counts()
        fig_productos = px.pie(values=productos.values, names=productos.index, title='Ventas por Línea de Producto')
        st.plotly_chart(fig_productos, use_container_width=True)

        # Mapa de Ventas por Ciudad
        m = folium.Map(location=[filtered_df['Ciudad'].mean(), filtered_df['Ciudad'].median()], zoom_start=5)
        for city, sales in filtered_df.groupby('Ciudad')['Total'].sum().items():
            folium.Marker(
                location=[filtered_df[filtered_df['Ciudad'] == city]['Ciudad'].mean(),
                          filtered_df[filtered_df['Ciudad'] == city]['Ciudad'].median()],
                popup=f"{city}: ${sales:,.2f}",
                icon=folium.Icon(color='red', icon='dollar-sign', prefix='fa')
            ).add_to(m)
        st_folium(m, width=800, height=500)

elif nav == "Tabla de Datos":
    # Tabla de Datos
    st.dataframe(filtered_df)

# Métodos de Pago
metodos_pago = filtered_df['Método de Pago'].value_counts()
fig_metodos_pago = px.pie(values=metodos_pago.values, names=metodos_pago.index, title='Métodos de Pago')
st.plotly_chart(fig_metodos_pago, use_container_width=True)