# CyberStill SIEM – Web & ESP32 Integration  
Sistema SIEM aplicado a entornos IoT con clasificación inteligente de eventos

---

## Descripción General

CyberStill SIEM Web & ESP32 Integration es un sistema de monitoreo de seguridad para entornos IoT, donde un dispositivo ESP32 actúa como generador de eventos, enviando comandos mediante el protocolo UDP a un servidor backend desarrollado en Python. Dicho servidor clasifica los eventos mediante un sistema básico de Inteligencia Artificial, los registra en archivos CSV, los envía a un SIEM local y los visualiza en tiempo real a través de una interfaz web.

Este proyecto representa la versión inicial del núcleo de CyberStill, orientado a la ciberseguridad defensiva aplicada a dispositivos IoT.

---

## Objetivo del Proyecto

- Integrar dispositivos IoT dentro de un entorno SIEM.
- Simular la detección de comandos sospechosos.
- Aplicar monitoreo centralizado y automatización de eventos.
- Servir como base para el desarrollo de una IA defensiva a mayor escala.

---

## Arquitectura del Sistema

ESP32 envia datos por UDP al servidor Python.  
El servidor clasifica mediante IA, registra en CSV, envía al SIEM y muestra en el dashboard web.

---

## Tecnologías Utilizadas

- Hardware: ESP32  
- Backend: Python 3.x, Flask  
- Protocolo: UDP  
- Frontend: HTML, CSS, JavaScript  
- IA: Clasificación básica de comandos  
- SIEM: Local (personalizado o ELK)  
- Logs: CSV  
- Red: WiFi  

---

## Características Principales

- Comunicación ESP32 a servidor por UDP.
- Clasificación automática mediante IA.
- Identificación de eventos sospechosos.
- Registro automático en CSV.
- Envío automático al SIEM.
- Visualización web en tiempo real.
- Arquitectura IoT funcional.
- Enfoque defensivo (Blue Team).

---

## Estructura del Proyecto

CyberStill-SIEM-Web/
├── backend/
├── fronted/
├── include/
├── lib/
├── src/
├── test/
├── requirements.txt
└── README.md


---

## Requisitos

### Software

- Python 3.x  
- Flask  
- requests  
- socket  

Instalación de dependencias:

```bash
pip install -r requirements.txt

Hardware

ESP32 configurado en la misma red que el backend.

SIEM

SIEM local ejecutándose en:

http://127.0.0.1:8080


API Key configurada para recepción de eventos.

Instalación y Ejecución
1. Clonar repositorio
git clone https://github.com/tu_usuario/CyberStill-SIEM-Web.git
cd CyberStill-SIEM-Web

2. Configurar IP del servidor en el ESP32

Dentro del código del ESP32:

const char* serverIP = "IP_DE_TU_PC";

3. Ejecutar servidor UDP
python backend/server_wifi_udp.py

4. Ejecutar aplicación web
python backend/app.py


Acceso a la web:

http://127.0.0.1:5000

Funcionamiento del Sistema

El ESP32 envía comandos al servidor mediante UDP.

El servidor clasifica los comandos usando IA.

Los eventos se almacenan en un archivo CSV.

Los eventos se envían al SIEM.

Los eventos se visualizan en el dashboard web.

Visualización

Desde la interfaz web se pueden observar:

Eventos en tiempo real.

Clasificación por nivel de riesgo.

Historial de tráfico IoT.

Simulación de ataques desde dispositivos IoT.

Enfoque en Ciberseguridad

Blue Team.

Monitoreo de red.

Detección de intrusos.

Automatización de seguridad.

IA aplicada a ciberseguridad.

Seguridad en entornos IoT.

Contexto Académico

Proyecto desarrollado para el curso:

BMA20P – Facultad de Ingeniería Eléctrica y Electrónica – Universidad Nacional de Ingeniería.

Contribuciones

Las contribuciones se realizan mediante Pull Requests.
Los errores pueden reportarse mediante Issues.

Licencia

MIT License.

Créditos

Proyecto desarrollado por CyberStill-GmbH.

Estado del Proyecto

Versión 1.0 – Operativa.
Versión 2.0 – IA mejorada (planificada).
Versión 3.0 – Predicción de ataques (planificada).
Versión SaaS – En desarrollo futuro.

Desarrollado por: CyberStill-GmbH
