# 🛒 Supermarket Data Analysis - Myanmar

Este proyecto tiene como objetivo realizar un **análisis integral de datos de un supermercado en Myanmar**, utilizando herramientas modernas de ciencia de datos, visualización interactiva y generación de reportes automatizados.

---

## 📊 Características principales

- **Análisis en Python**  
  
  - Notebooks de Jupyter para exploración, limpieza y modelado de datos.
  - Uso de librerías como `pandas`, `numpy`, `matplotlib`, `seaborn` y `scikit-learn`.

- **Visualización interactiva**  
  
  - Dash: dashboards dinámicos para análisis en tiempo real.  
  - Streamlit: aplicaciones web sencillas y rápidas para compartir resultados.

- **Invoicing (Generación de facturas)**  
  
  - Scripts automatizados para crear facturas en PDF.  
  - Integración con datos de ventas y clientes.

- **Reporting**  
  
  - Presentaciones en **PowerPoint** y reportes en **PDF** generados automáticamente.  
  - Resúmenes ejecutivos y visualizaciones clave para la toma de decisiones.

---

## 📂 Estructura del proyecto

```
├── data/                # Datos brutos y procesados
├── notebooks/           # Jupyter Notebooks de análisis
├── dashboards/          # Aplicaciones Dash y Streamlit
├── invoicing/           # Scripts para generación de facturas
├── reporting/           # Reportes en PDF y presentaciones PowerPoint
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación principal
```

---

## 🚀 Instalación y uso

1. Clona este repositorio:
   
   ```
   git clone https://github.com/LCPallares/supermarket_sales_myanmar.git
   cd supermarket_sales_myanmar
   ```

2. Instala las dependencias:
   
   ```
   pip install -r requirements.txt
   ```

3. Explora los notebooks:
   
   ```
   jupyter notebook notebooks/
   ```

4. Ejecuta las visualizaciones:
   
   - **Dash**:
     
     ```
     python dashboards/app_dash.py
     ```
   - **Streamlit**:
     
     ```
     streamlit run dashboards/app_streamlit.py
     ```

5. Genera facturas:
   
   ```
   python invoicing/generate_invoice.py
   ```

6. Crea reportes:
   
   ```
   python reporting/generate_report.py
   ```

---

## 📈 Ejemplos de análisis

- Tendencias de ventas por categoría de producto.  
- Comportamiento de clientes según ubicación y frecuencia de compra.  
- Comparación de ingresos mensuales y estacionalidad.  
- Visualización de métricas clave en dashboards interactivos.

---

## 🛠️ Tecnologías utilizadas

- **Lenguaje:** Python 3.x  
- **Data Analysis:** Pandas, NumPy, Scikit-learn  
- **Visualización:** Matplotlib, Seaborn, Dash, Streamlit  
- **Automatización:** ReportLab, python-pptx  
- **Entorno:** Jupyter Notebook

---

## 📌 Próximos pasos

- Implementar modelos predictivos de ventas.  
- Integrar análisis de clientes con segmentación avanzada.  
- Desplegar dashboards en la nube para acceso remoto.  

---

## 👤 Autor

Proyecto desarrollado por [Tu Nombre].  
Si tienes sugerencias o mejoras, ¡no dudes en abrir un **issue** o enviar un **pull request**!
