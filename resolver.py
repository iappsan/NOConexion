import socket
import time

HOST = "172.16.8.13"                # IP del Resolver
ROOTHOST = "172.16.8.23"            # IP del rootDNS
GLOBAL_PORT = 5432                  # El puerto que usa el servidor
BUFFERSIZE = 1024                   # Tamano del buffer
CLIENT_SOCKET = socket.socket()          # Iniciamos el socket
ROOT_SOCKET = socket.socket()            # Iniciamos el socket 2
CLIENT_SOCKET.bind((HOST, GLOBAL_PORT))  # Lo ligamos al host y al puerto
CLIENT_SOCKET.listen(10)                 # Definimos el numero de conecciones a escuchar
CLIENTS = []

def main():
    global CLIENTS
    global CLIENT_SOCKET
    global ROOT_SOCKET
    global GLOBAL_PORT
    TLD_SOCKET = socket.socket()
    MAS_SOCKET = socket.socket()

    while True:
        print('Esperando conexion')
        CONN, ADDR = CLIENT_SOCKET.accept()
        print(ADDR + ' conectado...\n')
        CLIENTS.append(CONN)

        rawAddress = str(CONN.recv(BUFFERSIZE).decode('UTF-8'))
        splitAddress = rawAddress.split('.')

        CONN.send(str.encode('Consultando servidor raiz...'))
        
        ROOT_SOCKET.connect((ROOTHOST, GLOBAL_PORT))
        ROOT_SOCKET.send(str.encode(splitAddress[-1]))

        rootRes = ROOT_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
        if (rootRes == 'ERR'):
            CONN.send(str.encode('No se encontro ningun TLD'))
        else:
            TLD_SOCKET.connect((rootRes,GLOBAL_PORT))
            CONN.send(str.encode('Consultando TLD '+rootRes))
            TLD_SOCKET.send(str.encode(splitAddress[-1]))

            TLDRes = TLD_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
            if (rootRes == 'ERR'):
                CONN.send(str.encode('No se encontro ningun servidor de nombres'))
            else:
                MAS_SOCKET.connect((TLDRes,GLOBAL_PORT))
                CONN.send(str.encode('Consultando TLD '+TLDRes))
                MAS_SOCKET.send(str.encode(rawAddress))

                MASRes = MAS_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
                if (MASRes == 'ERR'):
                    CONN.send(str.encode('No se encontro el dominio'))
                else:
                    str2 = 'El dominio '+rawAddress+' se encuentra en '+MASRes
                    CONN.send(str.encode(str2))
        
        stopConnections()

def stopConnections():
    global CLIENTS
    for c in CLIENTS:
        c.close()

if __name__ == '__main__':
    main()