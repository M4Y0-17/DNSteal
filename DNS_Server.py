#!/usr/bin/python

import socket
import dns.message
import dns.name
import dns.rdata
import dns.rdataclass
import dns.rdatatype
import dns.rrset
import binascii
from signal import signal, SIGINT
from sys import exit
import colorama
from colorama import Fore
import random
import argparse
import os
from os import stat



# Probamos si la carpeta existe y sino creamos una y devolvemos el valor del path
def create_mkdir(directory, folder):

	path = directory + folder
	try:
		os.mkdir(path)
		return path
	except:
		return path


# Comprueba que el nombre del nuevo archivo no esté cogido y si lo esta crea otro nombre hasta dar con uno que no lo esté
def check_name(path):

	random_name = ''
	random_name = random.randint(0, 99999)
	random_name = "bin_file__" + str(random_name) + ".txt"
	random_name = path + random_name

	try:
		with open((random_name), "rb") as f:
			check_name(path)
	except:
		print(Fore.MAGENTA + "Binary File: " + random_name)
		print(Fore.RESET)
		# Devolvemos el nuevo nombre del archivo para que podamos crearlo y escribir en él
		return random_name


# Probamos de desencriptar en hexadecimal y si no podemos imprimimos que el mensaje no esta en hexadecimal
def hex_to_txt(hex_txt):

	try:
		# Traducimos el mensaje de hexadecimal a ASCII
		hex_translated_message = bytearray.fromhex(hex_txt).decode('utf-8')
		print(Fore.CYAN + "\nMessage Decrypted:" + Fore.RESET)
		print(hex_translated_message)
	except:
		print(Fore.MAGENTA + "\nThe message is not in hexadecimal" + Fore.RESET)


def DNS_Server(server, domain, response_ip, port):

	buffer = 4096
	i = 0
	complete_message = ""

	end = "END_DNS"
	end = bytes(end, 'utf-8')
	end = binascii.hexlify(end)
	end = end.decode('UTF-8')

	# Creamos un socket UDP
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind((server, int(port)))


	print(Fore.GREEN + "\n  -|-  WAITING REQUESTS...  -|-  \n")
	print(Fore.RESET)

	while True:

		i = i + 1
		random_name = ""

		# Recibir peticiones
		request_data, client_address = server_socket.recvfrom(buffer)

		print(Fore.MAGENTA + "Package Nº", i)
		print(Fore.RESET)

		# Deserializar la peticion
		request = dns.message.from_wire(request_data)
		print(Fore.CYAN + "Request:" + Fore.RESET)
		print(request)

		# Extraemos el nombre de dominio de la peticion
		domain_name = request.question[0].name.to_text()
		print(Fore.CYAN + "\nDomain name:" + Fore.RESET)
		print(domain_name)

		# Extraemos el subdominio del dominio
		subdomain = domain_name.split(".")[0]
		print(Fore.CYAN + "\nReceived Subdomain:" + Fore.RESET)
		print(subdomain[:-1])

		# Pasamos el mensaje de hexadecimal a txt
		hex_to_txt(subdomain)

		# No añadimos el mensaje de finalizar el programa en el texto final
		if subdomain != end:
			complete_message = complete_message + subdomain

		# Creamos la respuesta del DNS vacía
		DNS_response = dns.message.make_response(request)
		# Hacemos que el ID de la respuesta sea el mismo que el de la petición
		DNS_response.id = request.id
		DNS_response.set_rcode(dns.rcode.NOERROR)

		# Juntamos la peticion del cliente con el nombre nuevo de dominio
		DNS_response.answer.append(dns.rrset.from_text(domain, 300, dns.rdataclass.IN, dns.rdatatype.A, response_ip))

		# Serializamos la respuesta
		response_data = DNS_response.to_wire()

		# Enviamos la respuesta al cliente
		server_socket.sendto(response_data, client_address)

		print("\n|------------------------------------------------------------|\n")

		# Cerramos el programa cuando llegue el texto de finalizar las peticiones
		if subdomain == end:
			# Al finalizar las peticiones escribimos en binario el mensaje enviado en un txt
			path = create_mkdir("./", "bin_data")
			path = str(path) + "/"

			random_name = check_name(path)

			# Creamos el archivo y escribimos en binario el texto que nos han enviado
			with open(random_name, "w") as bin_file:
				bin_file.write(bin(int(complete_message, 16)))
				bin_file.close()

			# Imprimimos el texto que estaba en hexadecimal en texto normal
			print(Fore.CYAN + "Final Message:")
			print(Fore.RESET)
			complete_message = bytearray.fromhex(complete_message).decode('utf-8')
			print(complete_message)

			# Contar cuantos bytes tiene el mensaje que hemos recibido
			bytes_file = len(complete_message)
			print(Fore.CYAN + "\nBytes that the received message has:" + Fore.RESET)
			print(bytes_file)

			finish_banner()


# Banner para finalizar el programa
def finish_banner():

	print(Fore.RED + "\n\n  -|-  ENDING...  -|-  ")
	print(Fore.RESET)
	exit(0)


# Funcion que cierra el programa cuando se presiona Ctrl + C
def finish(signal_received, frame):
	
	finish_banner()


# Banner que queda bien
def banner():

	this_file = '''        -------  SERVER  -------'''
	banner_tool='''    ____  _   _______ __             __
   / __ \/ | / / ___// /____  ____ _/ /
  / / / /  |/ /\__ \/ __/ _ \/ __ `/ / 
 / /_/ / /|  /___/ / /_/  __/ /_/ / /  
/_____/_/ |_//____/\__/\___/\__,_/_/   
	'''
	by = '''                            by Alex Mayo'''
	print("")
	print(Fore.GREEN + this_file)
	print(Fore.YELLOW + banner_tool)
	print(Fore.CYAN + by)
	print(Fore.RESET)


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--server', type=str, nargs=1, help='[Optional] IP you want for the server. Predet = 0.0.0.0')
	parser.add_argument('-d', '--domain', type=str, nargs=1, help='[Optional] Domain you want to use. Predet = secreto.com.')
	parser.add_argument('-i', '--ip', type=str, nargs=1, help='[Optional] Fake reply IP. Predet = 127.0.0.1')
	parser.add_argument('-p', '--port', type=str, nargs=1, help='[Optional] Port you want to use. Predet = 53')

	args = parser.parse_args()

	if args.server:
		ip = str(args.server)
		# ['127.0.0.1'] -> 127.0.0.1
		ip = ip[2:-2]
	else:
		ip = "0.0.0.0"

	if args.domain:
		domain = str(args.domain)
		# ['secreto.com'] -> secreto.com
		domain = domain[2:-2]
	else:
		domain = "secreto.com."

	if args.ip:
		response_ip = str(args.ip)
		# ['127.0.0.1'] -> 127.0.0.1
		response_ip = response_ip[2:-2]
	else:
		response_ip = "127.0.0.1"

	if args.port:
		port = str(args.port)
		# ['53'] -> 53
		port = port[2:-2]
	else:
		port = 53

	DNS_Server(ip, domain, response_ip, port)


if __name__ == '__main__':

	# Llamamos la funciona finish cuando se presione Ctrl + C
	signal(SIGINT, finish)
	banner()
	main()
