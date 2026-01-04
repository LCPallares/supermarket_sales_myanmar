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
    root = etree.Element("Factura", xmlns="http://www.ejemplo.com/factura")
    
    # Agregar información general de la factura
    etree.SubElement(root, "NumeroFactura").text = sale['Invoice ID']
    etree.SubElement(root, "Fecha").text = sale['Date'].strftime('%Y-%m-%d')
    etree.SubElement(root, "Hora").text = sale['Time']
    etree.SubElement(root, "UUID").text = str(uuid.uuid4())

    # Agregar información del cliente
    cliente = etree.SubElement(root, "Cliente")
    etree.SubElement(cliente, "Tipo").text = sale['Customer type']
    etree.SubElement(cliente, "Genero").text = sale['Gender']
    etree.SubElement(cliente, "ID").text = f"CUST-{str(uuid.uuid4())[:8]}"

    # Agregar información de la sucursal
    sucursal = etree.SubElement(root, "Sucursal")
    etree.SubElement(sucursal, "Ciudad").text = sale['City']
    etree.SubElement(sucursal, "Nombre").text = sale['Branch']
    etree.SubElement(sucursal, "Direccion").text = "123 Calle Principal"
    etree.SubElement(sucursal, "Telefono").text = "+1 234 567 8900"

    # Agregar detalles del producto
    productos = etree.SubElement(root, "Productos")
    producto = etree.SubElement(productos, "Producto")
    etree.SubElement(producto, "LineaProducto").text = sale['Product line']
    etree.SubElement(producto, "PrecioUnitario").text = str(sale['Unit price'])
    etree.SubElement(producto, "Cantidad").text = str(sale['Quantity'])
    etree.SubElement(producto, "Subtotal").text = str(sale['Unit price'] * sale['Quantity'])

    # Agregar información de pago
    pago = etree.SubElement(root, "Pago")
    etree.SubElement(pago, "Metodo").text = sale['Payment']
    etree.SubElement(pago, "CostoProductos").text = str(sale['Cost of goods sold'])
    etree.SubElement(pago, "Impuesto").text = str(sale['Tax 5%'])
    etree.SubElement(pago, "Total").text = str(sale['Total'])

    # Agregar términos y condiciones
    terminos = etree.SubElement(root, "TerminosCondiciones")
    etree.SubElement(terminos, "Politica").text = "Todos los productos tienen 30 días de garantía."
    etree.SubElement(terminos, "Devolucion").text = "Las devoluciones se aceptan dentro de los 14 días de la compra."

    # Crear el árbol XML
    tree = etree.ElementTree(root)
    
    # Generar un nombre de archivo único
    filename = f"factura_{sale['Invoice ID'].replace('/', '_')}.xml"
    
    # Guardar el archivo XML
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding='utf-8')
    
    return filename


def create_xslt():
    # Define the namespaces
    nsmap = {
        'xsl': 'http://www.w3.org/1999/XSL/Transform',
        None: 'http://www.w3.org/1999/xhtml'
    }
    
    # Create the root element with proper namespace handling
    xslt_root = etree.Element("{http://www.w3.org/1999/XSL/Transform}stylesheet",
                              attrib={"version": "1.0"},
                              nsmap=nsmap)

    etree.SubElement(xslt_root, "{http://www.w3.org/1999/XSL/Transform}output",
                     method="html", encoding="utf-8", indent="yes")

    template = etree.SubElement(xslt_root, "{http://www.w3.org/1999/XSL/Transform}template", match="/")
    html = etree.SubElement(template, "html")
    head = etree.SubElement(html, "head")
    etree.SubElement(head, "title").text = "Factura"
    style = etree.SubElement(head, "style")
    style.text = """
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
    """

    body = etree.SubElement(html, "body")
    etree.SubElement(body, "h1").text = "Factura"

    for section in ["NumeroFactura", "Fecha", "Hora", "UUID"]:
        etree.SubElement(body, "p").text = f"{section}: "
        etree.SubElement(body, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"Factura/{section}")

    for section in ["Cliente", "Sucursal", "Productos", "Pago", "TerminosCondiciones"]:
        etree.SubElement(body, "h2").text = section
        table = etree.SubElement(body, "table")
        # Create an XPath object
        xpath = etree.XPath(f"//Factura/{section}//*[not(*)]")
        # Use a dummy root element to evaluate the XPath
        dummy_root = etree.Element("Factura")
        section_elem = etree.SubElement(dummy_root, section)
        # Add some dummy child elements
        for i in range(3):
            child = etree.SubElement(section_elem, f"Field{i}")
            child.text = f"Value{i}"
        # Now evaluate the XPath on the dummy tree
        for field in xpath(dummy_root):
            tr = etree.SubElement(table, "tr")
            etree.SubElement(tr, "th").text = field.tag
            td = etree.SubElement(tr, "td")
            etree.SubElement(td, "{http://www.w3.org/1999/XSL/Transform}value-of", select=f"Factura/{section}/{field.tag}")

    # Create the XSLT tree
    xslt_tree = etree.ElementTree(xslt_root)
    
    # Save the XSLT file
    xslt_filename = "factura_style.xslt"
    xslt_tree.write(xslt_filename, pretty_print=True, xml_declaration=True, encoding='utf-8')
    
    return xslt_filename


# Cargar los datos
df = load_data()

# Generar una factura XML para la primera venta
sale = df.iloc[0]
#print(sale)

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
