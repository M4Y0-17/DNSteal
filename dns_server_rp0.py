#!/usr/bin/python
# Archivo ....: dns_client_rp0.py
# Autor ......: Roger Placín
# Revisado ...: G.M.
# Fecha ......: 16/12/2022
# Descripción : Programa que simula servidor DNS.
#               Solo reconoce estructura UDP, no cumple estrcutura DNS.

import socket
import dns.message
import dns.name
import dns.query


servidor = ('0.0.0.0', 53)
dominio = "secreto.com" 
inicio = '--- INICIO ---'       # Marca de Inicio
fin = '--- FIN ---'             # Marca de Fin
buffer = 4096                   # Buffer  

# Crea un socket UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Asigna una dirección y un puerto al socket
udp.bind(servidor)
print("Esperando peticiones...")

# Escucha indefinidamente hasta recibir el paquete FIN
while True:
    # Recibe datos
    data, addr = udp.recvfrom(buffer)
    # Obtiene el nombre del dominio a partir del byte 13 ya que el protocolo
    # UDP 
    mensaje = data[13:].decode() # El mensaje está a partir del byte 13

    print("Recibidos datos de la IP ", addr)
    print("Datos brutos ", data)
    print("Datos: ", mensaje)

    print(mensaje)
    print(addr)
    # Crea el paquete DNS de respuesta
    nombre_de_dominio = dns.name.from_text(dominio)

    # Esto [NO ES CORRECTO], pues pone una solicitud de dominio cuando esto
    # tendría que ser una respuesta, pues es el servidor, pero lo dejo
    # para que se vea lo que se envia.
    solicitud = dns.message.make_query(nombre_de_dominio, dns.rdatatype.A)

    # Enviar la solicitud al servidor DNS
    dns.query.send_udp(udp, solicitud, addr)
    
    # La condición de finalización también falla, pero ahora no es importante.
    if mensaje == fin:
        break