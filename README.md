# HoneyIoT

<div align="center">

**Sistema Honeypot Inteligente para Dispositivos IoT**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-ESP32-green.svg)](https://www.espressif.com/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

*Sistema SIEM aplicado a entornos IoT con clasificación inteligente de eventos*

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación)

</div>

---

## 📋 Tabla de Contenidos

- [Sobre el Proyecto](#-sobre-el-proyecto)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Visualización](#-visualización)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## 🎯 Sobre el Proyecto

**HoneyIoT** es un sistema SIEM (Security Information and Event Management) especializado en la monitorización y detección de amenazas en entornos IoT. Utiliza dispositivos ESP32 como honeypots inteligentes que capturan, analizan y clasifican comandos sospechosos mediante técnicas de inteligencia artificial.

### Objetivos Principales

- ✅ Integrar dispositivos IoT en un entorno SIEM centralizado
- ✅ Detectar y clasificar comandos sospechosos en tiempo real
- ✅ Automatizar el monitoreo y respuesta ante eventos de seguridad
- ✅ Proporcionar base para desarrollo de IA defensiva escalable

### Contexto Académico

Este proyecto fue desarrollado como parte del curso **BMA20P** en la **Facultad de Ingeniería Eléctrica y Electrónica** de la **Universidad Nacional de Ingeniería (UNI)**, con enfoque en ciberseguridad defensiva aplicada a IoT.

---

## ✨ Características

- 🛡️ **Honeypot IoT**: ESP32 actuando como señuelo para atraer y estudiar ataques
- 🤖 **Clasificación Inteligente**: IA para análisis automático de comandos maliciosos
- 📡 **Comunicación UDP**: Transmisión eficiente y de baja latencia
- 📊 **Dashboard en Tiempo Real**: Visualización instantánea de eventos de seguridad
- 💾 **Registro Persistente**: Almacenamiento estructurado en formato CSV
- 🔗 **Integración SIEM**: Compatible con sistemas SIEM locales (ELK Stack y otros)
- ⚡ **Arquitectura Escalable**: Diseño modular preparado para múltiples dispositivos
- 🔵 **Enfoque Blue Team**: Orientado a ciberseguridad defensiva

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│     ESP32       │
│   (Honeypot)    │
│                 │
│  WiFi Enabled   │
└────────┬────────┘
         │ UDP
         │ Comandos
         ▼
┌─────────────────────────────────────┐
│      Servidor Python Backend        │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Receptor UDP (port 8888)   │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │   Clasificador IA            │  │
│  │   (Análisis de comandos)     │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│       ┌─────┴─────┐                │
│       │           │                │
│       ▼           ▼                │
│  ┌────────┐  ┌─────────┐          │
│  │  CSV   │  │  SIEM   │          │
│  │  Logs  │  │  Local  │          │
│  └────────┘  └─────────┘          │
│       │                            │
│       ▼                            │
│  ┌──────────────────────────────┐  │
│  │   Flask Web Server           │  │
│  │   Dashboard (port 5000)      │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Navegador     │
│   Web (UI)      │
└─────────────────┘
```

### Flujo de Datos

1. **Captura**: ESP32 recibe comandos de red y los envía vía UDP
2. **Recepción**: Servidor backend escucha en puerto UDP 8888
3. **Clasificación**: Motor IA analiza y clasifica el nivel de amenaza
4. **Persistencia**: Eventos se registran en archivo CSV con timestamp
5. **Integración**: Datos se reenvían al SIEM local para correlación
6. **Visualización**: Dashboard web muestra eventos en tiempo real

---

## 🛠️ Tecnologías

### Hardware
- **ESP32**: Microcontrolador con WiFi/Bluetooth integrado
- **Sensores** (opcional): Para simulación de dispositivo IoT real

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.x | Lenguaje principal |
| Flask | Latest | Framework web |
| Socket | Built-in | Comunicación UDP |
| Pandas | Latest | Manejo de datos CSV |

### Frontend
- **HTML5/CSS3**: Estructura y diseño responsivo
- **JavaScript**: Interactividad y actualizaciones en tiempo real
- **Chart.js** (opcional): Visualización de métricas

### Seguridad & IA
- **Clasificador Custom**: Modelo de ML para detección de comandos maliciosos
- **SIEM Local**: Sistema de gestión de eventos (ELK Stack compatible)

### Protocolos
- **UDP**: Comunicación dispositivo-servidor
- **HTTP/WebSocket**: Comunicación servidor-dashboard

---

## 📦 Requisitos Previos

### Software

```bash
# Python 3.7 o superior
python --version

# pip (gestor de paquetes)
pip --version
```

### Hardware

- **ESP32** con WiFi configurado
- **PC/Servidor** en la misma red local
- **Red WiFi** con conectividad estable

### SIEM (Opcional)

Si deseas integración completa con SIEM:
- SIEM local ejecutándose en `http://127.0.0.1:8080`
- API Key configurada para recepción de eventos

---

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/HoneyIoT.git
cd HoneyIoT
```

### 2. Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
Flask>=2.0.0
requests>=2.26.0
pandas>=1.3.0
```

### 3. Configurar el ESP32

Abre el archivo de código del ESP32 (ubicado en `src/`) y modifica:

```cpp
// Configuración WiFi
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_CONTRASEÑA";

// IP del servidor backend
const char* serverIP = "192.168.1.X";  // Cambia por la IP de tu PC
const int serverPort = 8888;
```

### 4. Flashear el ESP32

Usando Arduino IDE o PlatformIO:

```bash
# Con PlatformIO
pio run --target upload
```

---

## ⚙️ Configuración

### Backend

Edita `backend/config.py` si es necesario:

```python
# Configuración del servidor UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 8888

# Configuración del SIEM
SIEM_URL = "http://127.0.0.1:8080/api/events"
SIEM_API_KEY = "tu_api_key_aqui"

# Archivo de logs
LOG_FILE = "logs/eventos.csv"
```

---

## 🎮 Uso

### Iniciar el Sistema

#### 1. Ejecutar Servidor UDP (Terminal 1)

```bash
cd backend
python server_wifi_udp.py
```

Salida esperada:
```
[INFO] Servidor UDP iniciado en 0.0.0.0:8888
[INFO] Esperando eventos del ESP32...
```

#### 2. Ejecutar Aplicación Web (Terminal 2)

```bash
cd backend
python app.py
```

Salida esperada:
```
[INFO] Dashboard web iniciado en http://127.0.0.1:5000
[INFO] Presiona CTRL+C para detener
```

#### 3. Acceder al Dashboard

Abre tu navegador y visita:
```
http://127.0.0.1:5000
```

### Verificar Funcionamiento

1. El ESP32 debe conectarse a la red WiFi
2. Comenzará a enviar comandos al servidor
3. Verás eventos aparecer en el dashboard en tiempo real
4. Los logs se guardarán en `logs/eventos.csv`

---

## 📁 Estructura del Proyecto

```
HoneyIoT/
│
├── backend/
│   ├── app.py                    # Aplicación Flask (Dashboard)
│   ├── server_wifi_udp.py        # Servidor UDP receptor
│   ├── classifier.py             # Motor de clasificación IA
│   ├── siem_integration.py       # Integración con SIEM
│   └── config.py                 # Configuraciones generales
│
├── frontend/
│   ├── index.html                # Página principal del dashboard
│   ├── css/
│   │   └── styles.css            # Estilos personalizados
│   └── js/
│       └── dashboard.js          # Lógica del dashboard
│
├── src/
│   └── esp32_honeypot.ino        # Código fuente del ESP32
│
├── include/
│   └── config.h                  # Configuraciones del ESP32
│
├── lib/
│   └── [librerías externas]      # Dependencias del ESP32
│
├── test/
│   ├── test_classifier.py        # Tests del clasificador
│   └── test_udp.py               # Tests de comunicación UDP
│
├── logs/
│   └── eventos.csv               # Registro de eventos (generado)
│
├── docs/
│   ├── ARCHITECTURE.md           # Documentación de arquitectura
│   └── API.md                    # Documentación de API
│
├── requirements.txt              # Dependencias de Python
├── platformio.ini                # Configuración PlatformIO (opcional)
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📊 Visualización

El dashboard web proporciona las siguientes vistas:

### Panel Principal

- **Eventos en Tiempo Real**: Stream de comandos capturados
- **Clasificación de Riesgo**: 
  - 🟢 Bajo (comandos normales)
  - 🟡 Medio (comandos sospechosos)
  - 🔴 Alto (comandos maliciosos)

### Métricas

- Total de eventos capturados
- Distribución por nivel de amenaza
- Comandos más frecuentes
- Línea temporal de actividad

### Historial

- Tabla interactiva con todos los eventos
- Filtros por fecha, tipo y severidad
- Exportación a CSV

---

## 🗺️ Roadmap

### ✅ Versión 1.0 (Actual - Operativa)
- [x] Comunicación UDP ESP32-Servidor
- [x] Clasificación básica de comandos
- [x] Dashboard web funcional
- [x] Registro en CSV
- [x] Integración SIEM básica

### 🔄 Versión 2.0 (En Planificación)
- [ ] Clasificador IA mejorado con ML
- [ ] Soporte para múltiples ESP32
- [ ] Base de datos SQL en lugar de CSV
- [ ] Sistema de alertas por email/Telegram
- [ ] API REST documentada

### 🚀 Versión 3.0 (Futuro)
- [ ] Predicción de ataques mediante Deep Learning
- [ ] Análisis de comportamiento anómalo
- [ ] Respuesta automática a amenazas
- [ ] Dashboard con mapas de calor geográfico

### 🌐 Versión SaaS (Visión a Largo Plazo)
- [ ] Plataforma cloud multi-tenant
- [ ] Modelos IA entrenados colaborativamente
- [ ] Marketplace de reglas de detección
- [ ] Integración con plataformas IoT comerciales

---

## 🤝 Contribución

Las contribuciones son bienvenidas y apreciadas. Para contribuir:

### 1. Fork del Proyecto

```bash
# Haz fork desde GitHub UI, luego:
git clone https://github.com/CyberStill-GmbH/HoneyIoT.git
cd HoneyIoT
```

### 2. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
```

### 3. Realizar Cambios

```bash
git add .
git commit -m "feat: descripción de la nueva funcionalidad"
```

### 4. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
# Luego crea un Pull Request en GitHub
```

### Directrices

- Sigue las convenciones de código existentes
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Describe claramente los cambios en el PR

### Reportar Bugs

Abre un [Issue](https://github.com/CyberStill-GmbH/HoneyIoT/issues) con:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla (si aplica)
- Información del sistema

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 CyberStill-GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Créditos

### Desarrollo

**HoneyIoT** es desarrollado y mantenido por **CyberStill-GmbH**

### Institución Académica

Proyecto desarrollado en colaboración con:
- **Universidad Nacional de Ingeniería (UNI)**
- **Facultad de Ingeniería Eléctrica y Electrónica (FIEE)**
- **Curso**: BMA20P

### Agradecimientos

- Docentes y personal de la FIEE-UNI
- Comunidad open source de ESP32
- Contribuidores del proyecto


## 🔗 Enlaces Útiles

- [Documentación de ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OWASP IoT Security](https://owasp.org/www-project-internet-of-things/)
- [Guía de Honeypots](https://www.sans.org/white-papers/36240/)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ por el equipo de CyberStill-GmbH

</div>


Desarrollado por: CyberStill-GmbH
