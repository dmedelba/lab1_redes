import socket as sock

#Función para crear un archivo por header consultado.
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

	#Se realiza el handshake para conexión con el servidor
	TCP_socketCliente.connect((dir_servidor, puerto_servidor))

	#Solicitamos la url al usuario
	url = input('Ingrese la URL: ')

	if(url.upper() == "TERMINATE"):
		flag= False
		TCP_socketCliente.send(url.encode()) #notificamos al servidor para que cierre la conexión
		TCP_socketCliente.close() #se cierra el socket cliente

	else:
		#enviamos el url al servidor para la consulta
		TCP_socketCliente.send(url.encode())
		puerto_z = TCP_socketCliente.recv(2048).decode()
		#print("la conexión UDP sera en el puerto",puerto_z)

		#conexión UDP con el servidor
		UDP_socketCliente = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		respuesta_conexion = "OK" #respondemos OK al servidor para la conexión UDP.
		UDP_socketCliente.sendto(respuesta_conexion.encode(),(dir_servidor,int(puerto_z)))

		#obtenemos el header mediante la respuesta por UDP del servidor.
		header, _ = UDP_socketCliente.recvfrom(2048)
		str_header = header.decode()
		
		nombre_archivo = url + ".txt"
		escribir_archivo(nombre_archivo,str_header) #creamos el archivo con el header

		UDP_socketCliente.close() #cerramos socket cliente	
