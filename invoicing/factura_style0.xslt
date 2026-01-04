<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" version="1.0">
  <xsl:output method="html" encoding="utf-8" indent="yes"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>Factura Electrónica</title>
        <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        .total { font-weight: bold; }
    </style>
      </head>
      <body>
        <h1>Factura Electrónica</h1>
        <h2>Información General</h2>
        <table>
          <tr>
            <th>Serie</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/Serie"/>
            </td>
          </tr>
          <tr>
            <th>Folio</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/Folio"/>
            </td>
          </tr>
          <tr>
            <th>Fecha</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/Fecha"/>
            </td>
          </tr>
          <tr>
            <th>FormaPago</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/FormaPago"/>
            </td>
          </tr>
          <tr>
            <th>SubTotal</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/SubTotal"/>
            </td>
          </tr>
          <tr>
            <th>Moneda</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/Moneda"/>
            </td>
          </tr>
          <tr>
            <th>Total</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/Total"/>
            </td>
          </tr>
          <tr>
            <th>TipoDeComprobante</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/TipoDeComprobante"/>
            </td>
          </tr>
          <tr>
            <th>MetodoPago</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/MetodoPago"/>
            </td>
          </tr>
          <tr>
            <th>LugarExpedicion</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Comprobante/LugarExpedicion"/>
            </td>
          </tr>
        </table>
        <h2>Emisor</h2>
        <table>
          <tr>
            <th>Rfc</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Emisor/Rfc"/>
            </td>
          </tr>
          <tr>
            <th>Nombre</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Emisor/Nombre"/>
            </td>
          </tr>
          <tr>
            <th>RegimenFiscal</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Emisor/RegimenFiscal"/>
            </td>
          </tr>
        </table>
        <h2>Receptor</h2>
        <table>
          <tr>
            <th>Rfc</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Receptor/Rfc"/>
            </td>
          </tr>
          <tr>
            <th>Nombre</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Receptor/Nombre"/>
            </td>
          </tr>
          <tr>
            <th>UsoCFDI</th>
            <td>
              <xsl:value-of select="FacturaElectronica/Receptor/UsoCFDI"/>
            </td>
          </tr>
        </table>
        <h2>Conceptos</h2>
        <table>
          <tr>
            <th>Cantidad</th>
            <th>Unidad</th>
            <th>Descripción</th>
            <th>Valor Unitario</th>
            <th>Importe</th>
          </tr>
          <tr>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Cantidad"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Unidad"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Descripcion"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/ValorUnitario"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Importe"/>
            </td>
          </tr>
        </table>
        <h2>Impuestos</h2>
        <table>
          <tr>
            <th>Base</th>
            <th>Impuesto</th>
            <th>Tipo Factor</th>
            <th>Tasa o Cuota</th>
            <th>Importe</th>
          </tr>
          <tr>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/Base"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/Impuesto"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/TipoFactor"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/TasaOCuota"/>
            </td>
            <td>
              <xsl:value-of select="FacturaElectronica/Conceptos/Concepto/Impuestos/Traslados/Traslado/Importe"/>
            </td>
          </tr>
        </table>
        <p class="total">Total: $<xsl:value-of select="FacturaElectronica/Comprobante/Total"/></p>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
