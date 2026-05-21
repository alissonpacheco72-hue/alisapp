# 📦 Sensor de Stock - Sistema IoT de Inventario

¡Bienvenido al proyecto **Sensor de Stock**! Este es un prototipo funcional académico diseñado bajo los principios de **Clean Architecture** para el control de inventarios físicos utilizando simulación de hardware y análisis de datos en la nube. 🚀

---

## 🎯 ¿Qué hace este proyecto?
El sistema simula un entorno donde los productos pasan por un arco de seguridad o puerta (sensor). Cuando se escanea o detecta un código QR, el sistema determina si el producto está entrando o saliendo del inventario.

- 🟢 **Entrada**: Se actualiza el inventario sumando la cantidad.
- 🔴 **Salida**: Se actualiza el inventario, pero físicamente (en la simulación) se dispara una alarma sonora (Buzzer) y visual (LED rojo).
- 📊 **Análisis**: Cada movimiento se registra en tiempo real y se envía a la nube para generar dashboards predictivos.

---

## 🛠️ Tecnologías Utilizadas

- 🐍 **Python & Streamlit**: Para la interfaz de usuario moderna (Dashboard y paneles de control).
- 🌐 **Wokwi**: Diagrama y simulación de hardware (ESP32, Sensor PIR, Buzzer, LED).
- ☁️ **Grafana Cloud & InfluxDB**: Para la ingesta de series de tiempo y visualización de datos (Dashboard analítico en la nube).
- 📓 **Google Colab (Jupyter)**: Para los análisis predictivos y modelos de datos históricos.
- 🏗️ **Clean Architecture**: Código dividido en Capas de Dominio, Casos de Uso, Controladores, Infraestructura e Interfaz.

---

## 🏗️ Arquitectura del Proyecto

```text
sensor_stock/
├── app.py                   # 🚪 Punto de entrada principal (Streamlit)
├── style.css                # 🎨 Estilos SaaS modernos
├── .streamlit/config.toml   # ⚙️ Configuración global de tema
├── domain/                  # 🧱 Entidades base (Product, Movement, Alert)
├── use_cases/               # 🧠 Lógica de negocio estricta
├── infrastructure/          # 🔌 Conexión a Base de datos CSV e InfluxDB Cloud
├── controllers/             # 🎛️ Orquestadores de información
├── interface/               # 🖥️ Vistas del usuario (Dashboard, Inventario, etc.)
└── data/                    # 🗄️ Base de datos local simulada (CSV)
```

---

## 🚀 Instalación y Uso (Local)

1. **Clonar e instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Correr la aplicación:**
   ```bash
   streamlit run app.py
   ```
3. **Explorar:** Se abrirá tu navegador en `http://localhost:8501`. Desde ahí puedes modificar el inventario como si fuera Excel, exportar CSVs y generar QRs.

---

## ☁️ Integración con Grafana Cloud (Analítica Avanzada)

Para cumplir con el análisis profundo de datos, este proyecto está configurado para conectarse a Grafana Cloud, descartando la necesidad de instalar motores pesados localmente.

### ¿Cómo configurarlo?
1. Crea una cuenta en [Grafana Cloud](https://grafana.com/).
2. Dentro de tu portal de Grafana Cloud, dirígete a **Access Policies** (Políticas de acceso) o **Tokens**.
3. Genera un **Cloud Access Policy Token** dándole permisos de escritura (Write).
4. Agrega tu `URL` y tu `Token` al archivo `infrastructure/influxdb_repository.py` del proyecto.
5. ¡Listo! Al registrar movimientos en Streamlit, los datos volarán automáticamente a tus paneles en la nube.

---

## 🔬 Análisis de Datos (Colab)
Dentro de los archivos del proyecto encontrarás `analisis_datos.ipynb`. Solo súbelo a **Google Colab** para correr las celdas y visualizar las frecuencias de movimiento y los gráficos de actividad predictiva exigidos en la rúbrica académica.

---
*Desarrollado para la presentación de integración IoT y Data Science.* ✨
