import socket as sock
def escribir_archivo(nombre_archivo,header):
	archivo = open(nombre_archivo,"w")
	archivo.write(header)
	archivo.close()

puerto_servidor =65000

dir_servidor = 'localhost'
flag= True

while(flag):
	#creamos el socket del cliente
	TCP_socketCliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

	#esta fuención realiza handshake
	TCP_socketCliente.connect((dir_servidor, puerto_servidor))

	url = input('Ingrese la URL: ')

	if(url.upper() == "TERMINATE"):
		TCP_socketCliente.send(url.encode())
		flag= False
	else:

		TCP_socketCliente.send(url.encode())
		puerto_z = TCP_socketCliente.recv(2048).decode()
		print("la conexión UDP sera en el puerto",puerto_z)


		#conexión UDP con el servidor
		UDP_socketCliente = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		respuesta_conexion = input("Para iniciar transferencia en el puerto Z ingrese OK: ")
		UDP_socketCliente.sendto(respuesta_conexion.encode(),(dir_servidor,int(puerto_z)))

		header, _ = UDP_socketCliente.recvfrom(2048)
		str_header = header.decode()
		#escribir el header en el .txt
		nombre_archivo = url + ".txt"
		escribir_archivo(nombre_archivo,str_header)

		print(str_header)
		UDP_socketCliente.close()

		
