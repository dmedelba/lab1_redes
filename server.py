import socket as sock

#Rango de puertos disponibles 9152-65535 
puerto_servidor =65000

#Función que agrega la tupla (url, header) al cache del servidor
def add_cache(lista, elemento):
    lista.insert(0,elemento)
    if len(lista) > 5:
        lista.pop(5)
    return

#Función que verifica si el url ya fue consultado, 
#retorna una tupla con el valor de la condición y el header
def in_cache(url, cache):
	for i in cache:
		if i[0] == url:
			header = i[1]
			cache.remove(i)
			cache.insert(0,i)
			return (True, header)
	return (False,'')

#creamos socket TCP
TCP_socketServ = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
TCP_socketServ.bind(('', puerto_servidor))
#indica que espera handshakes, parametro que indica cantidad maxima de cola

TCP_socketServ.listen(5) #Servidor comienza a escuchar siempre queda activo
print("Servidor TCP escuchando en puerto", puerto_servidor)

flag = True
cache  = []
termino = 0
while(flag):
	#se obtiene datos del cliente
	TCP_socketCliente, dirCliente = TCP_socketServ.accept()
	#se recibe la URL 
	url = TCP_socketCliente.recv(2048).decode()
	#print("Se recibio:", url)

	condicion, header_cache = in_cache(url,cache) #url esta en el cache?

	if (url.upper() == "TERMINATE"):
		TCP_socketCliente.close()
		termino =1
		#flag = False  se cerraría la conexión del servidor
	elif (condicion):
		header = header_cache
	else:
		#Se obtiene el header con conexión directa a la web mediante TCP
		httpServ = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		httpServ.connect((url, 80))
		consulta = "GET / HTTP/1.1\r\n\r\n" #Consulta http
		httpServ.send(consulta.encode())

		respuesta_consulta = httpServ.recv(2048)
		rc_decode = respuesta_consulta.decode().split("<") #obtenemos solo el header
		header= rc_decode[0].encode()
		add_cache(cache,(url,header)) #agregamos la respuesta al cache del servidor
		httpServ.close()

	if termino == 0: 

		#print(cache) #para visualizar su funcionamiento
		#se envia nuevo puerto donde existirá la conexión UDP
		puerto_z = '55000'
		#se responde por TCP
		TCP_socketCliente.send(puerto_z.encode())
		UDP_socketServ = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
		UDP_socketServ.bind(('', int(puerto_z)))
		#print("Servidor escuchando en el puerto", puerto_z)

		#ahora aqui escucha en el servidor UDP y recibe la respuesta OK del cliente.
		respuestaUDP, dirClienteUDP = UDP_socketServ.recvfrom(2048)
		respUDP = respuestaUDP.decode()
		if (respUDP == "OK"):
			#se envia el header al cliente
			UDP_socketServ.sendto(header, dirClienteUDP)
			UDP_socketServ.close()
	else:
		termino = 0
		#cuando el cliente ingresa "terminate" se finaliza su conexión pero el servidor sigue
		#activo esperando otro cliente.