import socket
import time

HOST = "172.16.8.25"                # IP del servMaster
GLOBAL_PORT = 5432                  # El puerto que usa el servidor
BUFFERSIZE = 1024                   # Tamano del buffer
SOCKET = socket.socket()          # Iniciamos el socket
SOCKET.bind((HOST, GLOBAL_PORT))  # Lo ligamos al host y al puerto
SOCKET.listen(10)                 # Definimos el numero de conecciones a escuchar
CLIENTS = []

def main():
    global CLIENTS
    global SOCKET
    global GLOBAL_PORT

    while True:
        ip_res = ''

        print("Leyendo txt ...")      
        RAW_TEXT = []           # Texto crudo
        PRO_TEXT = []
        FILEPATH = './files/'    # Ruta de archivo
        f = open (FILEPATH+'dominios.txt', 'r') #Lee archivo y ordena lineas
        CONTENIDO = f.readlines()
        for line in CONTENIDO:
            RAW_TEXT.append(line.replace('\n',''))
        f.close()
        for item in RAW_TEXT:
            PRO_TEXT.append(item.split())

        print('Esperando conexion (serverMaster)')
        CONN, ADDR = SOCKET.accept()
        print(str(ADDR) + ' conectado...\n')
        CLIENTS.append(CONN)

        tld = str(CONN.recv(BUFFERSIZE).decode('UTF-8'))

        for item in RAW_TEXT:
            PRO_TEXT.append(item.split())

        for item in PRO_TEXT:
            if item[0] == tld:
                ip_res = item[-1]
                break

        if (len(ip_res) > 0):
            print('Repuesta: '+ ip_res)
            CONN.send(str.encode(ip_res))
        else:
            print('No se encontro nada')
            CONN.send(str.encode('ERR'))

        stopConnections()   


def stopConnections():
    global CLIENTS
    for c in CLIENTS:
        c.close()

if __name__ == '__main__':
    main()