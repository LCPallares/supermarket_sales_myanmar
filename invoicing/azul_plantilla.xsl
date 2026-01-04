<?xml version="1.0" encoding="UTF-8"?>
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
                .factura {
                    background: white;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    border-radius: 8px;
                }
                .cabecera {
                    background: #4a90e2;
                    color: white;
                    padding: 20px;
                    border-radius: 8px 8px 0 0;
                    text-align: center;
                }
                .info-tienda {
                    text-align: center;
                    margin: 20px 0;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }
                .detalles {
                    margin: 20px 0;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 15px;
                }
                .productos {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                .productos th {
                    background: #4a90e2;
                    color: white;
                    padding: 10px;
                }
                .productos td {
                    padding: 10px;
                    border-bottom: 1px solid #dee2e6;
                }
                .total {
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    text-align: right;
                    font-size: 1.2em;
                    margin-top: 20px;
                }
                .pie {
                    text-align: center;
                    margin-top: 20px;
                    color: #6c757d;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="factura">
                <div class="cabecera">
                    <h1>FACTURA</h1>
                    <div>Nº: <xsl:value-of select="factura/cabecera/invoice_id"/></div>
                </div>

                <div class="info-tienda">
                    <h2>Sucursal <xsl:value-of select="factura/cabecera/sucursal"/> - <xsl:value-of select="factura/cabecera/ciudad"/></h2>
                    <p>Fecha: <xsl:value-of select="factura/cabecera/fecha"/></p>
                    <p>Hora: <xsl:value-of select="factura/cabecera/hora"/></p>
                </div>

                <div class="detalles">
                    <h3>Información del Cliente:</h3>
                    <p>Tipo de Cliente: <xsl:value-of select="factura/cliente/tipo"/></p>
                    <p>Género: <xsl:value-of select="factura/cliente/genero"/></p>
                    <p>Rating: <xsl:value-of select="factura/cliente/rating"/></p>
                </div>

                <table class="productos">
                    <tr>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unitario</th>
                        <th>Total</th>
                    </tr>
                    <tr>
                        <td><xsl:value-of select="factura/venta/producto/linea"/></td>
                        <td><xsl:value-of select="factura/venta/producto/cantidad"/></td>
                        <td>$<xsl:value-of select="factura/venta/producto/precio_unitario"/></td>
                        <td>$<xsl:value-of select="factura/venta/producto/total"/></td>
                    </tr>
                </table>

                <div class="total">
                    <p>Subtotal: $<xsl:value-of select="factura/venta/costo_bienes"/></p>
                    <p>Impuesto (5%): $<xsl:value-of select="factura/venta/producto/impuesto"/></p>
                    <p><strong>TOTAL: $<xsl:value-of select="factura/venta/producto/total"/></strong></p>
                </div>

                <div class="pie">
                    <p>Método de pago: <xsl:value-of select="factura/venta/metodo_pago"/></p>
                    <p>Margen bruto: <xsl:value-of select="factura/venta/margen_porcentaje"/>%</p>
                    <p>Ingreso bruto: $<xsl:value-of select="factura/venta/ingreso_bruto"/></p>
                </div>
            </div>
        </body>
    </html>
</xsl:template>
</xsl:stylesheet>