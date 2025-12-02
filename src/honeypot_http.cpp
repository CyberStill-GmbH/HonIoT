#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiUdp.h>

// -------------------- CONFIGURACIÓN --------------------
#define WIFI_SSID       "Adrian"
#define WIFI_PASSWORD   ""

#define PC_IP   "10.168.146.253"
#define PC_PORT 6000

WebServer server(80);
WiFiUDP udp;

IPAddress pcIPAddress;

// -------------------- LEDS --------------------
const int LED1 = 2;
const int LED2 = 15;

bool led1State = false;
bool led2State = false;


// -------------------- WIFI --------------------
void conectarWiFi() {
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
  Serial.print("IP del ESP32: ");
  Serial.println(WiFi.localIP());
}


// -------------------- REENVÍO UDP --------------------
void reenviarComando(const String &cmd) {
  Serial.print("[HONEY] Comando recibido: ");
  Serial.println(cmd);

  udp.beginPacket(pcIPAddress, PC_PORT);
  udp.print(cmd);
  udp.endPacket();
}


// -------------------- ENDPOINT /send (solo POST) --------------------
void handleSend() {
  if (!server.hasArg("cmd")) {
    server.send(400, "text/plain", "Falta parametro cmd");
    return;
  }

  String cmd = server.arg("cmd");
  reenviarComando(cmd);

  server.send(200, "text/plain", "OK");
}


// -------------------- HTML --------------------
void sendHtml() {

  String response = R"rawliteral(
<!DOCTYPE html><html>
<head>
<title>ESP32 Web Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html { font-family: sans-serif; text-align: center; }
  body { display: inline-flex; flex-direction: column; }
  h1 { margin-bottom: 1.2em; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; grid-gap: 1em; margin-bottom: 2em; }
  .btn { background-color: #5B5; border: none; color: white; padding: 0.5em 1em; font-size: 1.5em; cursor: pointer; }
  .OFF { background-color: #333; }
  input { padding: 0.5em; font-size: 1.2em; width: 80%; }
</style>

<script>
function enviarComando() {
    let cmd = document.getElementById("cmdInput").value;

    fetch('/send', {
        method: 'POST',
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "cmd=" + encodeURIComponent(cmd)
    }).then(r => console.log("Comando enviado:", cmd));
}
</script>
</head>

<body>
<h1>ESP32 Web Server</h1>

<div class="grid">
  <h2>LED 1</h2>
  <a href="/toggle/1" class="btn LED1_TEXT">LED1_TEXT</a>

  <h2>LED 2</h2>
  <a href="/toggle/2" class="btn LED2_TEXT">LED2_TEXT</a>
</div>

<h2>Enviar comando</h2>
<input id="cmdInput" type="text" placeholder="Ingresa comando...">
<button class="btn" onclick="enviarComando()">Enviar</button>

</body>
</html>
)rawliteral";

  response.replace("LED1_TEXT", led1State ? "ON" : "OFF");
  response.replace("LED2_TEXT", led2State ? "ON" : "OFF");

  server.send(200, "text/html", response);
}


// -------------------- SERVER HTTP --------------------
void configurarServidorHTTP() {
  
  server.on("/", HTTP_GET, [](){ sendHtml(); });

  server.on("/toggle/1", HTTP_GET, []() {
    led1State = !led1State;
    digitalWrite(LED1, led1State);
    reenviarComando("toggle/1");
    sendHtml();
  });

  server.on("/toggle/2", HTTP_GET, []() {
    led2State = !led2State;
    digitalWrite(LED2, led2State);
    reenviarComando("toggle/2");
    sendHtml();
  });

  server.on("/send", HTTP_POST, handleSend);

  server.begin();
  Serial.println("Servidor HTTP iniciado");
}


// -------------------- SETUP --------------------
void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  conectarWiFi();

  pcIPAddress.fromString(PC_IP);
  udp.begin(6000);

  configurarServidorHTTP();
}


// -------------------- LOOP --------------------
void loop() {
  server.handleClient();
}
