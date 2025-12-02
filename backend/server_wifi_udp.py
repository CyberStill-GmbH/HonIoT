import socket
import requests  # <--- nuevo: para hacer POST al SIEM

from clasificador import clasificar
from logger_csv import get_logger

BUFFER_SIZE = 8192

# === Configuración del SIEM ===
SIEM_URL = "http://127.0.0.1:8080/siem/api/ingest"
SIEM_API_KEY = "9071840a83400733a9ca4a99febe59658e038602ba8f4ba7b1569e7366e48127" #Colocar token generado


def enviar_a_siem(source_ip: str, cmd: str, label: str, score: float, reason: str) -> None:
    """
    Envía el evento al backend SIEM.
    No lanza excepción si falla: solo imprime el error.
    """
    payload = {
        "source_ip": source_ip,
        "raw_cmd": cmd,
        "label": label or "desconocido",
        "score": float(score) if score is not None else 0.0,
        "reason": reason or "",
        # "extra": {...}  # si algún día quieres mandar más metadatos
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": SIEM_API_KEY,
    }

    try:
        resp = requests.post(SIEM_URL, json=payload, headers=headers, timeout=2)
        if resp.status_code != 201:
            # No rompemos el servidor UDP, solo avisamos por consola
            print(f"[SIEM] Error {resp.status_code}: {resp.text}")
        else:
            data = resp.json()
            event_id = data.get("event_id")
            print(f"[SIEM] Evento registrado, id={event_id}")
    except Exception as e:
        print(f"[SIEM] No se pudo enviar evento: {e}")


def run_udp_server(host: str = '192.168.18.41', port: int = 6000, ack: bool = True):
    logger = get_logger()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))  # Escucha en la IP y puerto especificados
    print(f'Servidor UDP escuchando en {host}:{port}')

    try:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)  # Espera a recibir datos
            source_ip, source_port = addr[0], addr[1]  # Dirección de origen

            try:
                cmd = data.decode('utf-8', errors='ignore')  # Decodifica el comando recibido
            except Exception:
                cmd = repr(data)  # Si hay un error en la decodificación, muestra los datos sin procesar

            # Clasifica el comando recibido
            res = clasificar(cmd)
            label = res.get('label')
            score = res.get('score', 0.0)
            reason = res.get('reason', '')

            # Registra la acción en el archivo de logs (CSV local)
            logger.log(source_ip, cmd, label, score, reason)
            print(f"[UDP] {source_ip} -> {label} (score={score:.2f}) : {cmd.strip()}")

            # Envía también el evento al SIEM
            enviar_a_siem(source_ip, cmd, label, score, reason)

            # Envía ACK de vuelta al origen (opcional)
            if ack:
                ack_msg = f'ACK:{label}:{score:.2f}'  # Prepara un mensaje de confirmación
                try:
                    sock.sendto(ack_msg.encode(), addr)  # Envía el ACK de vuelta al origen
                except Exception:
                    pass
    except KeyboardInterrupt:
        print('Servidor detenido por usuario')
    finally:
        sock.close()  # Cierra el socket cuando termine


if __name__ == '__main__':
    run_udp_server(host='192.168.18.41', port=6000)  # Especifica la IP y puerto al iniciar
