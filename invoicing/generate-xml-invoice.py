import pandas as pd
from lxml import etree
from datetime import datetime
import uuid

def load_data():
    df = pd.read_csv("supermarket_Sales.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def generate_xml_invoice(sale):
    # Crear el elemento raíz
    root = etree.Element("FacturaElectronica", xmlns="http://www.sat.gob.mx/cfd/3")
    
    # Información general de la factura
    comprobante = etree.SubElement(root, "Comprobante")
    etree.SubElement(comprobante, "Serie").text = "A"
    etree.SubElement(comprobante, "Folio").text = sale['Invoice ID']
    etree.SubElement(comprobante, "Fecha").text = f"{sale['Date'].strftime('%Y-%m-%d')}T{sale['Time']}"
    etree.SubElement(comprobante, "FormaPago").text = "01"  # 01 = Efectivo
    etree.SubElement(comprobante, "SubTotal").text = str(sale['Total'] - sale['Tax 5%'])
    etree.SubElement(comprobante, "Moneda").text = "MXN"
    etree.SubElement(comprobante, "Total").text = str(sale['Total'])
    etree.SubElement(comprobante, "TipoDeComprobante").text = "I"  # I = Ingreso
    etree.SubElement(comprobante, "MetodoPago").text = "PUE"  # PUE = Pago en una sola exhibición
    etree.SubElement(comprobante, "LugarExpedicion").text = "12345"  # Código postal del lugar de expedición

    # Información del emisor (la tienda)
    emisor = etree.SubElement(root, "Emisor")
    etree.SubElement(emisor, "Rfc").text = "XAXX010101000"  # RFC genérico
    etree.SubElement(emisor, "Nombre").text = sale['Branch']
    etree.SubElement(emisor, "RegimenFiscal").text = "601"  # 601 = General de Ley Personas Morales

    # Información del receptor (el cliente)
    receptor = etree.SubElement(root, "Receptor")
    etree.SubElement(receptor, "Rfc").text = "XAXX010101000"  # RFC genérico
    etree.SubElement(receptor, "Nombre").text = f"Cliente {sale['Customer type']}"
    etree.SubElement(receptor, "UsoCFDI").text = "G01"  # G01 = Adquisición de mercancías

    # Conceptos (productos)
    conceptos = etree.SubElement(root, "Conceptos")
    concepto = etree.SubElement(conceptos, "Concepto")
    etree.SubElement(concepto, "ClaveProdServ").text = "01010101"  # Clave genérica
    etree.SubElement(concepto, "Cantidad").text = str(sale['Quantity'])
    etree.SubElement(concepto, "ClaveUnidad").text = "H87"  # Pieza
    etree.SubElement(concepto, "Unidad").text = "Pieza"
    etree.SubElement(concepto, "Descripcion").text = sale['Product line']
    etree.SubElement(concepto, "ValorUnitario").text = str(sale['Unit price'])
    etree.SubElement(concepto, "Importe").text = str(sale['Total'] - sale['Tax 5%'])

    # Impuestos
    impuestos = etree.SubElement(concepto, "Impuestos")
    traslados = etree.SubElement(impuestos, "Traslados")
    traslado = etree.SubElement(traslados, "Traslado")
    etree.SubElement(traslado, "Base").text = str(sale['Total'] - sale['Tax 5%'])
    etree.SubElement(traslado, "Impuesto").text = "002"  # 002 = IVA
    etree.SubElement(traslado, "TipoFactor").text = "Tasa"
    etree.SubElement(traslado, "TasaOCuota").text = "0.160000"
    etree.SubElement(traslado, "Importe").text = str(sale['Tax 5%'])

    # Crear el árbol XML
    tree = etree.ElementTree(root)
    
    # Generar un nombre de archivo único
    filename = f"factura_{sale['Invoice ID'].replace('/', '_')}.xml"
    
    # Guardar el archivo XML
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding='utf-8')
    
    return filename

def create_xslt():
    nsmap = {
        'xsl': 'http://www.w3.org/1999/XSL/Transform',
        None: 'http://www.w3.org/1999/xhtml'
    }
    
    xslt_root = etree.Element("{http://www.w3.org/1999/XSL/Transform}stylesheet",
                              attrib={"version": "1.0"},
                              nsmap=nsmap)

    etree.SubElement(xslt_root, "{http://www.w3.org/1999/XSL/Transform}output",
                     method="html", encoding="utf-8", indent="yes")

    template = etree.SubElement(xslt_root, "{http://www.w3.org/1999/XSL/Transform}template", match="/")
    html = etree.SubElement(template, "html")
    head = etree.SubElement(html, "head")
    etree.SubElement(head, "title").text = "Factura Electrónica"
    style = etree.SubElement(head, "style")
    style.text = """
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { font-weight: bold; }
    """

    body = etree.SubElement(html, "body")
    etree.SubElement(body, "h1").text = "Factura Electrónica"

    # Información general
    etree.SubElement(body, "h2").text = "Información General"
    info_table = etree.SubElement(body, "table")
    for field in ["Serie", "Folio", "Fecha", "FormaPago", "SubTotal", "Moneda", "Total", "TipoDeComprobante", "MetodoPago", "LugarExpedicion"]:
        tr = etree.SubElement(info_table, "tr")
        etree.SubElement(tr, "th").text = field
        td = etree.SubElement(tr, "td")
        etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"FacturaElectronica/Comprobante/{field}")

    # Emisor
    etree.SubElement(body, "h2").text = "Emisor"
    emisor_table = etree.SubElement(body, "table")
    for field in ["Rfc", "Nombre", "RegimenFiscal"]:
        tr = etree.SubElement(emisor_table, "tr")
        etree.SubElement(tr, "th").text = field
        td = etree.SubElement(tr, "td")
        etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"FacturaElectronica/Emisor/{field}")

    # Receptor
    etree.SubElement(body, "h2").text = "Receptor"
    receptor_table = etree.SubElement(body, "table")
    for field in ["Rfc", "Nombre", "UsoCFDI"]:
        tr = etree.SubElement(receptor_table, "tr")
        etree.SubElement(tr, "th").text = field
        td = etree.SubElement(tr, "td")
        etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"FacturaElectronica/Receptor/{field}")

    # Conceptos
    etree.SubElement(body, "h2").text = "Conceptos"
    conceptos_table = etree.SubElement(body, "table")
    tr = etree.SubElement(conceptos_table, "tr")
    for header in ["Cantidad", "Unidad", "Descripción", "Valor Unitario", "Importe"]:
        etree.SubElement(tr, "th").text = header
    
    tr = etree.SubElement(conceptos_table, "tr")
    for field in ["Cantidad", "Unidad", "Descripcion", "ValorUnitario", "Importe"]:
        td = etree.SubElement(tr, "td")
        etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"FacturaElectronica/Conceptos/Concepto/{field}")

    # Impuestos
    etree.SubElement(body, "h2").text = "Impuestos"
    impuestos_table = etree.SubElement(body, "table")
    tr = etree.SubElement(impuestos_table, "tr")
    for header in ["Base", "Impuesto", "Tipo Factor", "Tasa o Cuota", "Importe"]:
        etree.SubElement(tr, "th").text = header
    
    tr = etree.SubElement(impuestos_table, "tr")
    for field in ["Base", "Impuesto", "TipoFactor", "TasaOCuota", "Importe"]:
        td = etree.SubElement(tr, "td")
        etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/{field}")

    # Total
    total_p = etree.SubElement(body, "p", attrib={"class": "total"})
    total_p.text = "Total: $"
    etree.SubElement(total_p, "{http://www.w3.org/1999/XSL/Transform}value-of", select="FacturaElectronica/Comprobante/Total")

    xslt_tree = etree.ElementTree(xslt_root)
    xslt_filename = "factura_style.xslt"
    xslt_tree.write(xslt_filename, pretty_print=True, xml_declaration=True, encoding='utf-8')
    
    return xslt_filename

# Cargar los datos
df = load_data()

# Generar una factura XML para la primera venta
sale = df.iloc[0]
xml_filename = generate_xml_invoice(sale)

# Crear el archivo XSLT
xslt_filename = create_xslt()

print(f"Factura XML generada: {xml_filename}")
print(f"Archivo XSLT generado: {xslt_filename}")

# Añadir referencia al XSLT en el XML
parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse(xml_filename, parser)
xslt_pi = etree.ProcessingInstruction("xml-stylesheet", f'type="text/xsl" href="{xslt_filename}"')
tree.getroot().addprevious(xslt_pi)
tree.write(xml_filename, pretty_print=True, xml_declaration=True, encoding='utf-8')

print("Referencia XSLT añadida al XML. Ahora puedes abrir el XML en un navegador para una mejor visualización.")