import socket as sock

#Rango de puertos 49152-65535

puerto_servidor =65000

#creamos socket TCP bruch
TCP_socketServ = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
TCP_socketServ.bind(('', puerto_servidor))
#indica que espera handshakes, parametro que indica cantidad maxima de cola

#Servidor comienza a escuchar siempre queda activo.
TCP_socketServ.listen(5) #para el manejo de cache LRU
print("Servidor TCP escuchando en puerto", puerto_servidor)

flag = True

while(flag):
	#solo recibe archivos comunicación
	TCP_socketCliente, dirCliente = TCP_socketServ.accept()
	#se recibe la URL 
	url = TCP_socketCliente.recv(2048).decode()
	print("Se recibio:", url)
	if (url.upper() == "TERMINATE"):
		flag = False
		#se finaliza la conexión del servidor
	else:
		#Se obtiene el header 
		header = "ESTE SERIA EL HEADER"
		#se envia nuevo puerto donde existirá la conexión UDP
		puerto_z = '55000'
		#se responde por TCP
		TCP_socketCliente.send(puerto_z.encode())
		UDP_socketServ = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		UDP_socketServ.bind(('', int(puerto_z)))
		print("Servidor escuchando en el puerto", puerto_z)
		#ahora aqui escucha en el servidor UDP y recibe.
		respuestaUDP, dirClienteUDP = UDP_socketServ.recvfrom(2048)
		respUDP = respuestaUDP.decode()
		if (respUDP.upper() != "OK"):
			print("respuesta no es la esperada")
		else:
			#se envia el header al cliente
			UDP_socketServ.sendto(header.encode(), dirClienteUDP)
			UDP_socketServ.close()
		#recibe OK y le envia el header
		#se genera una nueva conexión UDP
		#enviar header de URL mediante UDP

		#aqui crear ciclo hasta que diga terminate.

		#ver el cierre 
		TCP_socketCliente.close()
