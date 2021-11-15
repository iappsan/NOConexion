import socket
from threading import Thread

HOST = "172.16.8.13"        #Direccion del Resolver
PORT = 5432                 #Puerto del Resolver
BUFFERSIZE = 1024
MYSOCKET = socket.socket()

def receive():              #Recibe una actualizacion
    global MYSOCKET
    global BUFFERSIZE
    
    while True:
        try:
            RESPONSE = MYSOCKET.recv(BUFFERSIZE).decode('UTF-8')
            if(len(RESPONSE) > 0):
                print (RESPONSE)
        except OSError:
            print("ERROR")
            break

def main():
    global HOST
    global PORT
    global MYSOCKET

    MYSOCKET.connect((HOST, PORT))
    RECV_THREAD = Thread(target=receive)
    RECV_THREAD.start()

    print('Bienvenido a la consulta')

    print('Direccion a consultar: ')
    addr = input()
    MYSOCKET.send(str.encode(addr))
    
    MYSOCKET.close()
    print('Hasta luego')

if __name__ == '__main__':
    main()