import pandas as pd
import xml.etree.ElementTree as ET

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

def clean_column_name(name):
    # Reemplazar espacios por guiones bajos y eliminar caracteres no válidos
    name = name.replace(' ', '_')
    name = name.replace('%', 'Porcentaje')  # Reemplaza % por Porcentaje
    name = name.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') # Quitar tildes
    name = name.replace('ñ', 'n')  # Reemplaza ñ por n
    return name

def crear_xml(df):
    root = ET.Element("Facturas")

    for _, row in df.iterrows():
        factura = ET.SubElement(root, "Factura")
        
        for field in df.columns:
            clean_name = clean_column_name(field)
            elemento = ET.SubElement(factura, clean_name)
            elemento.text = str(row[field])
    
    # Convertir el árbol a un string de XML
    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Guardar el XML en un archivo
    with open("facturas.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

    print("Archivo XML generado: facturas.xml")

crear_xml(df)
