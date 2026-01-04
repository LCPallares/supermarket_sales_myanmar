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
        
        return ET.tostring(self.root, encoding='unicode')

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

def generar_factura_xml(fila):
    template = crear_plantilla_personalizada()
    
    # Crear el documento XML
    xml_factura = template.generate_xml(fila.to_dict())
    
    # Crear el documento XML completo con la declaración XML y la referencia XSL
    xml_completo = f'''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="factura_style.xsl"?>
{xml_factura}'''
    
    nombre_archivo = f"factura_{fila['ID de Factura']}.xml"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(xml_completo)
    
    print(f"Factura generada: {nombre_archivo}")


def crear_xsl_basico():
    xsl_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <head>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
          }
          .invoice {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
          }
          h1 {
            color: #333;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
          }
          .section {
            margin-bottom: 20px;
          }
          .section-title {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 10px;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
          }
          th {
            background-color: #f2f2f2;
          }
          .highlight {
            font-weight: bold;
            color: #007bff;
          }
        </style>
      </head>
      <body>
        <div class="invoice">
          <h1>Factura #<xsl:value-of select="Factura/Encabezado/IDFactura"/></h1>
          
          <div class="section">
            <div class="section-title">Información General</div>
            <table>
              <tr>
                <th>Fecha</th>
                <td><xsl:value-of select="Factura/Encabezado/Fecha"/></td>
                <th>Hora</th>
                <td><xsl:value-of select="Factura/Encabezado/Hora"/></td>
              </tr>
            </table>
          </div>
          
          <div class="section">
            <div class="section-title">Información del Cliente</div>
            <table>
              <tr>
                <th>Tipo de Cliente</th>
                <td><xsl:value-of select="Factura/InformacionCliente/Tipo"/></td>
              </tr>
              <tr>
                <th>Género</th>
                <td><xsl:value-of select="Factura/InformacionCliente/Genero"/></td>
              </tr>
              <tr>
                <th>Calificación</th>
                <td><xsl:value-of select="Factura/InformacionCliente/Calificacion"/></td>
              </tr>
            </table>
          </div>
          
          <div class="section">
            <div class="section-title">Datos de la Sucursal</div>
            <table>
              <tr>
                <th>Nombre</th>
                <td><xsl:value-of select="Factura/DatosSucursal/Nombre"/></td>
              </tr>
              <tr>
                <th>Ciudad</th>
                <td><xsl:value-of select="Factura/DatosSucursal/Ciudad"/></td>
              </tr>
            </table>
          </div>
          
          <div class="section">
            <div class="section-title">Detalles del Producto</div>
            <table>
              <tr>
                <th>Línea de Producto</th>
                <td><xsl:value-of select="Factura/DetallesProducto/LineaProducto"/></td>
              </tr>
              <tr>
                <th>Precio Unitario</th>
                <td>$<xsl:value-of select="Factura/DetallesProducto/PrecioUnitario"/></td>
              </tr>
              <tr>
                <th>Cantidad</th>
                <td><xsl:value-of select="Factura/DetallesProducto/Cantidad"/></td>
              </tr>
            </table>
          </div>
          
          <div class="section">
            <div class="section-title">Información Financiera</div>
            <table>
              <tr>
                <th>Impuesto (5%)</th>
                <td>$<xsl:value-of select="Factura/InformacionFinanciera/Impuesto"/></td>
              </tr>
              <tr>
                <th>Total</th>
                <td class="highlight">$<xsl:value-of select="Factura/InformacionFinanciera/Total"/></td>
              </tr>
              <tr>
                <th>Método de Pago</th>
                <td><xsl:value-of select="Factura/InformacionFinanciera/MetodoPago"/></td>
              </tr>
              <tr>
                <th>Costo de Bienes Vendidos</th>
                <td>$<xsl:value-of select="Factura/InformacionFinanciera/CostoBienesVendidos"/></td>
              </tr>
              <tr>
                <th>Porcentaje de Margen Bruto</th>
                <td><xsl:value-of select="Factura/InformacionFinanciera/PorcentajeMargenBruto"/>%</td>
              </tr>
              <tr>
                <th>Ingreso Bruto</th>
                <td>$<xsl:value-of select="Factura/InformacionFinanciera/IngresoBruto"/></td>
              </tr>
            </table>
          </div>
        </div>
      </body>
    </html>
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
    
    # Generar la factura XML
    generar_factura_xml(sale)
    
    print("Proceso completado. Se ha generado una factura XML con referencia a XSL.")