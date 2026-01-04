from lxml import etree
import weasyprint

# Cargar el archivo XML y la hoja de estilo XSLT
xml_path = 'factura_750-67-8428.xml'
xslt_path = 'factura_style.xslt'

with open(xml_path, 'rb') as xml_file:
    xml_tree = etree.parse(xml_file)

with open(xslt_path, 'rb') as xslt_file:
    xslt_tree = etree.parse(xslt_file)
    transform = etree.XSLT(xslt_tree)

# Aplicar la transformación XSLT al XML
html_tree = transform(xml_tree)

# Convertir el HTML resultante a PDF
html_string = etree.tostring(html_tree, pretty_print=True).decode()

pdf_file = 'factura_750-67-8428.pdf'
weasyprint.HTML(string=html_string).write_pdf(pdf_file)

print(f'PDF generado: {pdf_file}')
