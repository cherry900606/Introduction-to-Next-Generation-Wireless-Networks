from socket import *
import threading
import string

# 計算所有連線client數量
connected_client_num = 0


# 將 n1,n2,n3 SPO 字串指令切割為數字 n1, n2 與 n3 回傳
def splitLength(sentence):
    sentence = sentence.split(' ')[0]
    s = sentence.split(',')
    return int(s[0]), int(s[1]), int(s[2])

# 將 account:password 字串切割回傳
def splitUserInformation(sentence):
    s = sentence.split(':')
    return s[0], s[1]

# 決定三邊長是否能組成三角形，以及三角形的種類
def determineTraingle(a, b, c):
    l = [a, b, c]
    l.sort()

    if l[0]+l[1] > l[2]:
        if l[0]**2 + l[1]**2 == l[2]**2:
            return 'Right Triangle'
        elif l[0]**2 + l[1]**2 > l[2]**2:
            return 'Acute Triangle'
        else:
            return 'Obtuse Triangle'
    else:
        return 'This is not a triangle'

# 將指令切格為前面的input，與後面的command類型
def read_sentence(sentence):
    s = sentence.split()[0]
    command = sentence.split()[1]
    return s, command

# 將字串進行 shift-two 的凱薩解密
def decrypt(s):
  decrypted_message = ""
  for c in s:
    if c in string.ascii_uppercase:
      position = string.ascii_uppercase.find(c)
      new_position = (position - 2) % 26
      new_character = string.ascii_uppercase[new_position]
      decrypted_message += new_character
    if c in string.ascii_lowercase:
      position = string.ascii_lowercase.find(c)
      new_position = (position - 2) % 26
      new_character = string.ascii_lowercase[new_position]
      decrypted_message += new_character
    if c in string.digits:
      position = string.digits.find(c)
      new_position = (position - 2) % 10
      new_character = string.digits[new_position]
      decrypted_message += new_character
  return decrypted_message


# 讀入使用者的帳號密碼，同時將密碼解密，以 dict 儲存
def user_data():
    info = {}
    with open('account_data.txt', mode='r') as file:
        for line in file:
            (account, password) = line.strip('\n').split(', ')
            info[account] = decrypt(password)
    return info

# 使用者連線
def on_new_client(connectionSocket, user_info):
    # 更新當前連線 client 的數量
    global connected_client_num
    connected_client_num += 1
    print('Accept {} connect.'.format(connected_client_num))
    
    login = False # 預設為未登入
    while True:
        sentence = connectionSocket.recv(1024).decode()
        s, command = read_sentence(sentence)

        # compute
        if command == "SPO":
            # 若未登入，則不執行該指令
            if not login:
                connectionSocket.send("Permission denied".encode())
                print('No permission to the triangle problem. Please try again.')

            # 讀檔
            elif s.find('.txt') != -1:
                with open(s, mode='r') as file:
                    content = file.readlines()
                    for line in content:
                        a, b, c = splitLength(line)
                        type = determineTraingle(a, b, c)
                        print('Triangle side lengths {}, {} and {} form {}'.format(a,b,c,type))
                        connectionSocket.send(type.encode())
            # 直接計算
            else:
                a, b, c = splitLength(s)
                type = determineTraingle(a, b, c)

                print('Triangle side lengths {}, {} and {} form {}'.format(a,b,c,type))
                connectionSocket.send(type.encode())
            #執行完指令後，關閉連線
            print('close the TCP socket connection of client \'{}\''.format(account))
            connectionSocket.send("finish".encode())
            connectionSocket.close()
            connected_client_num -= 1
            break
        # 使用者登入
        elif command == "LOGIN":
            account, password = splitUserInformation(s)
            if account in user_info and user_info[account] == password:
                connectionSocket.send("Valid".encode())
                login = True
                print('Client \'{}\' logins successfully.'.format(account))
            else:
                connectionSocket.send("Invalid".encode())
                print('Client \'{}\' is unregistered or enter incorrect password.'.format(account))
        else:
            print('error input')

        

serverPort = 12000
serverHost = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(1)
print('The server is ready to provide service.')
print('The maximun number of connection is 10.')

# 讀入使用者資料
user_info = user_data()

while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        threading.Thread(target=on_new_client, args=(connectionSocket, user_info)).start()

        
    except KeyboardInterrupt:
        break

serverSocket.shutdown
serverSocket.close()