import socket as sock

#Rango de puertos 49152-65535

puerto_servidor =65000

def add_cache(lista, elemento):
    lista.insert(0,elemento)
    if len(lista) > 5:
        lista.pop(5)
    return

def in_cache(url, cache):
#verifica si el elemento ya se encuentra en el cach
	for i in cache:
		if i[0] == url:
			header = i[1]
			cache.remove(i)
			cache.insert(0,i)
			return (True, header)
	return (False,'')



#creamos socket TCP bruch
TCP_socketServ = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
TCP_socketServ.bind(('', puerto_servidor))
#indica que espera handshakes, parametro que indica cantidad maxima de cola

#Servidor comienza a escuchar siempre queda activo.
TCP_socketServ.listen(5) #para el manejo de cache LRU
print("Servidor TCP escuchando en puerto", puerto_servidor)

flag = True
cache  = []

while(flag):
	#solo recibe archivos comunicación
	TCP_socketCliente, dirCliente = TCP_socketServ.accept()
	#se recibe la URL 
	url = TCP_socketCliente.recv(2048).decode()
	print("Se recibio:", url)

	if (url.upper() == "TERMINATE"):
		TCP_socketCliente.close()
		#flag = False
		#se finaliza la conexión del servidor
		#obtener su header y moficiar posicion de cache
	condicion, header_cache = in_cache(url,cache)
	if (condicion):
		header = header_cache
	else:
		#Se obtiene el header con conexión directa a la web
		httpServ = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		httpServ.connect((url, 80))
		consulta = "GET / HTTP/1.1\r\n\r\n"
		httpServ.send(consulta.encode())

		respuesta_consulta = httpServ.recv(2048)
		rc_decode = respuesta_consulta.decode().split("<")
		header= rc_decode[0].encode()
		add_cache(cache,(url,header))
		httpServ.close()

	print(cache)	
		
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
	if (respUDP == "OK"):
		#se envia el header al cliente
		UDP_socketServ.sendto(header, dirClienteUDP)
		UDP_socketServ.close()
	#recibe OK y le envia el header
	#se genera una nueva conexión UDP
	#enviar header de URL mediante UDP

	#aqui crear ciclo hasta que diga terminate.

		#ver el cierre 
		TCP_socketCliente.close()
