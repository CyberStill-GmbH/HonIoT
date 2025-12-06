Sistema Honeypot en ESP32 con cClasificación Inteligente de Comandos

Este proyecto consiste en la integración de una Web SIEM con un backend de servidor UDP, que recibe comandos enviados desde un dispositivo ESP32 y registra eventos en tiempo real. El sistema está diseñado para detectar y gestionar posibles amenazas de seguridad mediante inteligencia artificial (IA) para clasificar los comandos y enviar los eventos al SIEM (Security Information and Event Management) local.

Descripción

El proyecto CyberStill SIEM Web permite la integración de la detección de eventos desde dispositivos IoT (en este caso, un ESP32) con un backend web que gestiona estos eventos en tiempo real y los envía a un sistema SIEM para su posterior análisis.

El servidor UDP que recibe los comandos de los dispositivos IoT (ESP32) clasifica estos comandos utilizando un sistema de IA, registrándolos en un archivo CSV y también enviándolos al SIEM para su visualización.

Características principales:

Clasificación de comandos: Utiliza IA para identificar comandos sospechosos y peligrosos.

Web SIEM: Interfaz web para visualizar los eventos de seguridad registrados.

Servidor UDP: Permite que el ESP32 envíe datos al servidor.

Integración con SIEM: Envío de eventos al SIEM para su análisis.

Logs en CSV: Registro local de eventos en un archivo CSV para auditoría.

Estructura del Proyecto

El repositorio está dividido en las siguientes carpetas principales:

backend: Contiene el servidor UDP y la lógica para recibir y procesar los datos de los dispositivos IoT.

fronted: Código del frontend de la interfaz web para visualizar los eventos registrados por el SIEM.

include: Archivos de configuración y dependencias necesarias para la integración con el ESP32.

lib: Librerías adicionales para la comunicación con el backend y SIEM.

src: Archivos fuente para la aplicación web y la integración con el backend.

test: Archivos de prueba para asegurar la funcionalidad del sistema.

Requisitos

Python 3.x con las siguientes bibliotecas:

Flask (para el servidor web)

requests (para hacer solicitudes POST al SIEM)

socket (para gestionar el servidor UDP)

ESP32: Programado con el firmware adecuado para enviar comandos UDP al servidor.

Base de datos: Un sistema SIEM (como ELK, Splunk o un SIEM personalizado) para procesar y visualizar los eventos enviados desde el servidor UDP.

Instalación

Clona el repositorio:

git clone https://github.com/tu_usuario/CyberStill-SIEM-Web.git
cd CyberStill-SIEM-Web


Instalar dependencias:

Asegúrate de tener Python 3 instalado, luego instala las dependencias:

pip install -r requirements.txt


Configura el SIEM:

Asegúrate de tener tu SIEM configurado y corriendo en http://127.0.0.1:8080.

Asegúrate de generar un API Key para poder enviar eventos al SIEM.

Configura el ESP32:

Cambia la IP del servidor en el código del ESP32 a la dirección IP de tu máquina donde está corriendo el backend.

Asegúrate de que el ESP32 esté en la misma red que el servidor.

Ejecuta el servidor UDP:

Inicia el servidor backend que recibirá los comandos del ESP32:

python backend/server_wifi_udp.py


Inicia la aplicación web:

Si deseas usar la interfaz web para visualizar los eventos:

python backend/app.py


Esto iniciará la aplicación web en http://127.0.0.1:5000.

Uso

Envío de eventos desde el ESP32:

Una vez que todo esté configurado, el ESP32 enviará comandos UDP al servidor backend cada vez que detecte algo relevante. Los eventos serán clasificados y enviados al SIEM para su análisis.

Interfaz Web:

Puedes acceder a la interfaz web del SIEM para ver los eventos en tiempo real:

URL: http://127.0.0.1:5000

En la web podrás ver los eventos clasificados por el sistema de IA.

Visualización y análisis en SIEM:

Los eventos también serán registrados en tu SIEM y podrás analizarlos a través de las herramientas que uses para ello (por ejemplo, ElasticSearch, Kibana, o Splunk).

Contribuciones

Si deseas contribuir a este proyecto, puedes hacerlo mediante la creación de pull requests con mejoras o correcciones. Si encuentras algún bug, abre un issue para reportarlo.

Licencia

Este proyecto está bajo la licencia MIT License.

Créditos

Desarrollado por: CyberStill-GmbH
