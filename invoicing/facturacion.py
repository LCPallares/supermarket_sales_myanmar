import streamlit as st
import pandas as pd
from datetime import datetime
import jinja2

# Configuración de la página
st.set_page_config(page_title="Sistema de Facturación", layout="wide")

def cargar_datos():
    # Carga el CSV
    df = pd.read_csv('supermarket_sales.csv')
    # Renombrar columnas para mantener consistencia
    columnas = {
        'Invoice ID': 'Invoice_ID',
        'Branch': 'Branch',
        'City': 'City',
        'Customer type': 'Customer_type',
        'Gender': 'Gender',
        'Product line': 'Product_line',
        'Unit price': 'Unit_price',
        'Quantity': 'Quantity',
        'Tax 5%': 'Tax_5',
        'Total': 'Total',
        'Date': 'Date',
        'Time': 'Time',
        'Payment': 'Payment',
        'Cost of goods sold': 'cogs',
        'Gross margin percentage': 'gross_margin_percentage',
        'Gross income': 'gross_income',
        'Rating': 'Rating'
    }
    df = df.rename(columns=columnas)
    return df

def generar_html_factura(datos_factura):
    template_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            .factura { max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; }
            .cabecera { background: #4a90e2; color: white; padding: 20px; text-align: center; }
            .info-tienda { text-align: center; margin: 20px 0; }
            .detalles { margin: 20px 0; }
            .productos { width: 100%; border-collapse: collapse; margin: 20px 0; }
            .productos th { background: #4a90e2; color: white; padding: 10px; }
            .productos td { padding: 10px; border-bottom: 1px solid #ddd; }
            .total { text-align: right; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="factura">
            <div class="cabecera">
                <h1>FACTURA</h1>
                <div>Nº: {{ datos['Invoice_ID'] }}</div>
            </div>

            <div class="info-tienda">
                <h2>Sucursal {{ datos['Branch'] }} - {{ datos['City'] }}</h2>
                <p>Fecha: {{ datos['Date'] }}</p>
                <p>Hora: {{ datos['Time'] }}</p>
            </div>

            <div class="detalles">
                <h3>Información del Cliente:</h3>
                <p>Tipo de Cliente: {{ datos['Customer_type'] }}</p>
                <p>Género: {{ datos['Gender'] }}</p>
                <p>Rating: {{ datos['Rating'] }}</p>
            </div>

            <table class="productos">
                <tr>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Precio Unitario</th>
                    <th>Total</th>
                </tr>
                <tr>
                    <td>{{ datos['Product_line'] }}</td>
                    <td>{{ datos['Quantity'] }}</td>
                    <td>${{ "%.2f"|format(datos['Unit_price']) }}</td>
                    <td>${{ "%.2f"|format(datos['Total']) }}</td>
                </tr>
            </table>

            <div class="total">
                <p>Subtotal: ${{ "%.2f"|format(datos['Total'] - datos['Tax_5']) }}</p>
                <p>Impuesto (5%): ${{ "%.2f"|format(datos['Tax_5']) }}</p>
                <p><strong>TOTAL: ${{ "%.2f"|format(datos['Total']) }}</strong></p>
            </div>

            <div class="pie" style="text-align: center; margin-top: 20px;">
                <p>Método de pago: {{ datos['Payment'] }}</p>
                <p>Margen bruto: {{ "%.2f"|format(datos['gross_margin_percentage']) }}%</p>
                <p>Ingreso bruto: ${{ "%.2f"|format(datos['gross_income']) }}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = jinja2.Template(template_string)
    html_out = template.render(datos=datos_factura)
    return html_out

def main():
    st.title("🧾 Sistema de Facturación")
    
    try:
        df = cargar_datos()
        st.success("Datos cargados correctamente")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {str(e)}")
        return

    st.sidebar.header("Filtros")
    
    sucursales = df['Branch'].unique()
    sucursal = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)
    
    fechas = pd.to_datetime(df['Date']).dt.date.unique()
    fecha = st.sidebar.selectbox("Seleccionar Fecha", sorted(fechas))
    
    df_filtrado = df[
        (df['Branch'] == sucursal) & 
        (pd.to_datetime(df['Date']).dt.date == fecha)
    ]
    
    st.subheader("Facturas Disponibles")
    if len(df_filtrado) == 0:
        st.warning("No hay facturas para los filtros seleccionados")
    else:
        tabla_resumen = df_filtrado[['Invoice_ID', 'Customer_type', 'Product_line', 'Total']]
        st.dataframe(tabla_resumen)
        
        factura_seleccionada = st.selectbox(
            "Seleccionar factura para ver detalles",
            df_filtrado['Invoice_ID']
        )
        
        if factura_seleccionada:
            datos_factura = df_filtrado[df_filtrado['Invoice_ID'] == factura_seleccionada].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Detalles de la Factura")
                st.write(f"**Cliente:** {datos_factura['Customer_type']}")
                st.write(f"**Producto:** {datos_factura['Product_line']}")
                st.write(f"**Cantidad:** {datos_factura['Quantity']}")
                st.write(f"**Total:** ${datos_factura['Total']:.2f}")
            
            with col2:
                st.subheader("Información Adicional")
                st.write(f"**Método de Pago:** {datos_factura['Payment']}")
                st.write(f"**Impuesto:** ${datos_factura['Tax_5']:.2f}")
                st.write(f"**Margen Bruto:** {datos_factura['gross_margin_percentage']:.2f}%")
            
            if st.button("Generar Factura"):
                html_factura = generar_html_factura(datos_factura)
                st.components.v1.html(html_factura, height=600)
                
                st.download_button(
                    label="Descargar Factura HTML",
                    data=html_factura,
                    file_name=f"factura_{factura_seleccionada}.html",
                    mime="text/html"
                )

if __name__ == "__main__":
    main()