import socket
import time

HOST = "172.16.8.13"                # IP del Resolver
ROOTHOST = "172.16.8.23"            # IP del rootDNS
GLOBAL_PORT = 5432                  # El puerto que usa el servidor
BUFFERSIZE = 1024                   # Tamano del buffer
CLIENT_SOCKET = socket.socket()          # Iniciamos el socket
CLIENT_SOCKET.bind((HOST, GLOBAL_PORT))  # Lo ligamos al host y al puerto
CLIENT_SOCKET.listen(10)                 # Definimos el numero de conecciones a escuchar
CLIENTS = []
CACHE = []
CACHEAddr = []

def main():
    global CLIENTS
    global CLIENT_SOCKET
    global GLOBAL_PORT
    global BUFFERSIZE
    global CACHE

    ROOT_SOCKET = socket.socket()
    TLD_SOCKET = socket.socket()
    MAS_SOCKET = socket.socket()

    print('Esperando conexion (resolver)')
    CONN, ADDR = CLIENT_SOCKET.accept()
    print(str(ADDR) + ' conectado...\n')
    CLIENTS.append(CONN)

    ROOT_SOCKET.connect((ROOTHOST, GLOBAL_PORT))
    BOOLCONTINUE = True
    inCache = False

    while BOOLCONTINUE:
        inCache = False
        rawAddress = str(CONN.recv(BUFFERSIZE).decode('UTF-8'))
        if rawAddress == 'exit':
            BOOLCONTINUE = False
        
        print("direccion recibida: "+rawAddress)
        try:
            print(CACHE.index(rawAddress))
            inCache = True
            str2 = 'El dominio '+rawAddress+' se encuentra en '+MASRes
            print(str2)
            CONN.send(str.encode(str2))
        except:
            pass

        if not inCache:
            splitAddress = rawAddress.split('.')

            CONN.send(str.encode('Consultando servidor raiz...'))
            print('Consultando servidor raiz...')
            
            ROOT_SOCKET.send(str.encode(splitAddress[-1]))

            rootRes = ROOT_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
            if (rootRes == 'ERR'):
                print('No se encontro ningun TLD')
                CONN.send(str.encode('No se encontro ningun TLD'))
            else:
                TLD_SOCKET.connect((rootRes,GLOBAL_PORT))
                CONN.send(str.encode('Consultando TLD '+str(rootRes)))
                print('Consultando TLD '+rootRes)
                TLD_SOCKET.send(str.encode(splitAddress[-1]))

                TLDRes = TLD_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
                TLD_SOCKET.close()
                if (rootRes == 'ERR'):
                    print('No se encontro ningun servidor de nombres')
                    CONN.send(str.encode('No se encontro ningun servidor de nombres'))
                else:
                    MAS_SOCKET.connect((TLDRes,GLOBAL_PORT))
                    CONN.send(str.encode('Consultando TLD '+str(TLDRes)))
                    print('Consultando TLD '+TLDRes)
                    MAS_SOCKET.send(str.encode(rawAddress))

                    MASRes = MAS_SOCKET.recv(BUFFERSIZE).decode('UTF-8')
                    MAS_SOCKET.close()
                    if (MASRes == 'ERR'):
                        print('No se encontro ningun dominio')
                        CONN.send(str.encode('No se encontro el dominio'))
                    else:
                        CACHE.append(rawAddress)
                        CACHEAddr.append(MASRes)
                        str2 = 'El dominio '+rawAddress+' se encuentra en '+MASRes
                        print(str2)
                        CONN.send(str.encode(str2))
            
    stopConnections()

def stopConnections():
    global CLIENTS
    for c in CLIENTS:
        c.close()

if __name__ == '__main__':
    main()