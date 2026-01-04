import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

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

class XMLInvoiceTemplate:
    def __init__(self):
        self.root = ET.Element("Factura")
        self.structure = {}

    def add_element(self, path, field_name):
        parts = path.split('/')
        current = self.root
        for part in parts[:-1]:
            if part not in self.structure:
                self.structure[part] = ET.SubElement(current, part)
            current = self.structure[part]
        self.structure[path] = ET.SubElement(current, parts[-1])
        self.structure[path].set('field', field_name)

    def generate_xml(self, data):
        for element in self.root.iter():
            if 'field' in element.attrib:
                field = element.attrib['field']
                if field in data:
                    element.text = str(data[field])
                del element.attrib['field']
        
        xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="  ")
        return xmlstr

def crear_plantilla_personalizada():
    template = XMLInvoiceTemplate()
    
    # Definir la estructura de la plantilla
    template.add_element("Encabezado/IDFactura", "ID de Factura")
    template.add_element("Encabezado/Fecha", "Fecha")
    template.add_element("Encabezado/Hora", "Hora")
    
    template.add_element("InformacionCliente/Tipo", "Tipo de Cliente")
    template.add_element("InformacionCliente/Genero", "Género")
    template.add_element("InformacionCliente/Calificacion", "Calificación de Estratificación del Cliente")
    
    template.add_element("DatosSucursal/Nombre", "Sucursal")
    template.add_element("DatosSucursal/Ciudad", "Ciudad")
    
    template.add_element("DetallesProducto/LineaProducto", "Línea de Producto")
    template.add_element("DetallesProducto/PrecioUnitario", "Precio Unitario")
    template.add_element("DetallesProducto/Cantidad", "Cantidad")
    
    template.add_element("InformacionFinanciera/Impuesto", "Impuesto 5%")
    template.add_element("InformacionFinanciera/Total", "Total")
    template.add_element("InformacionFinanciera/MetodoPago", "Método de Pago")
    template.add_element("InformacionFinanciera/CostoBienesVendidos", "Costo de Bienes Vendidos")
    template.add_element("InformacionFinanciera/PorcentajeMargenBruto", "Porcentaje de Margen Bruto")
    template.add_element("InformacionFinanciera/IngresoBruto", "Ingreso Bruto")
    
    return template

def generar_facturas_xml(df):
    template = crear_plantilla_personalizada()
    
    for _, row in df.iterrows():
        # Crear el documento XML
        xml_factura = template.generate_xml(row.to_dict())
        
        # Agregar la instrucción de procesamiento XSL
        xml_con_xsl = f'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/xsl" href="factura_style.xsl"?>\n{xml_factura}'
        
        nombre_archivo = f"factura_{row['ID de Factura']}.xml"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(xml_con_xsl)
        print(f"Factura generada: {nombre_archivo}")


def generar_factura_xml(fila):
    template = crear_plantilla_personalizada()
    
    # Crear el documento XML
    xml_factura = template.generate_xml(fila.to_dict())
    
    # Agregar la instrucción de procesamiento XSL (si es necesario)
    xml_con_xsl = f'<?xml version="1.0" encoding="UTF-8"?>\n<?xml-stylesheet type="text/xsl" href="factura_style.xsl"?>\n{xml_factura}'
    
    nombre_archivo = f"factura_{fila['ID de Factura']}.xml"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(xml_con_xsl)
    
    print(f"Factura generada: {nombre_archivo}")


def crear_xsl_basico():
    xsl_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; }
          table { border-collapse: collapse; width: 100%; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #f2f2f2; }
        </style>
      </head>
      <body>
        <h1>Factura</h1>
        <xsl:apply-templates/>
      </body>
    </html>
  </xsl:template>
  
  <xsl:template match="*">
    <h2><xsl:value-of select="name()"/></h2>
    <table>
      <xsl:for-each select="*">
        <tr>
          <th><xsl:value-of select="name()"/></th>
          <td><xsl:value-of select="text()"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
</xsl:stylesheet>
"""
    with open("factura_style.xsl", "w", encoding="utf-8") as f:
        f.write(xsl_content)
    print("Archivo XSL básico creado: factura_style.xsl")

if __name__ == "__main__":
    # Cargar los datos
    df = load_data()
    
    # Crear el archivo XSL básico
    crear_xsl_basico()

    # Generar una factura XML para la primera venta
    sale = df.iloc[0]
    
    # Generar las facturas XML
    #generar_facturas_xml(df)
    generar_factura_xml(sale)
    
    #print(f"Proceso completado. Se han generado {len(df)} facturas XML con referencia a XSL.")
    print(f"Proceso completado. Se han generado factura XML con referencia a XSL.")