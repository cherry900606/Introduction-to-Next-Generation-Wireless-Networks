from socket import *

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    sentence = input('input: ')
    clientSocket.send(sentence.encode())
    if sentence == 'close':
        break

    response = clientSocket.recv(1024)
    print('From Server:', response.decode())
clientSocket.close()

