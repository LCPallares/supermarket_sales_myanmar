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
