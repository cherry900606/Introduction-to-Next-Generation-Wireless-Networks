from socket import *

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('input: ')
clientSocket.send(sentence.encode())

while True:
    response = clientSocket.recv(1024)

    # 結束連線
    if response.decode().find("finish") != -1:
        clientSocket.close()
        break

    # 接收 server 訊息
    print('From Server:', response.decode())
    if response.decode() == "Valid" or response.decode() == "Invalid":
        sentence = input('input: ')
        clientSocket.send(sentence.encode())
    

