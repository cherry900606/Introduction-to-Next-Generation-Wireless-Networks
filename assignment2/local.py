from socket import *
import json
import numpy as np

# record 紀錄 ip 跟 domain name
class Record:
    def __init__(self, ip_address, domain_name):
        self.ip_address = ip_address
        self.domain_name = domain_name
record_queue = []
victom = 0 # FIFO
counter = np.zeros(5) # LRU
count = 0 # LRU

# 讀 json 檔
file = open('local_DNS_data.json')
data = json.load(file)
file.close()
for index, item in enumerate(data):
    record = Record(item['ip_address'], item['domain_name'])
    record_queue.append(record)
    counter[index] = count # LRU
    count += 1

file = open('FIFO.json')
victom = json.load(file)
file.close()

file = open('LRU.json')
counter = np.array(json.load(file))
file.close()
count = np.max(counter) + 1

# LRU：找 counter 中數值最小的 index
def index_replace():
    index = 0
    for i in range(5):
        if counter[index] > counter[i]:
            index = i
    return index

# 從 record_queue 找 local server 有沒有紀錄
def get_ip(domain_name):
    global victom
    global count

    # 如果 local server 就有，直接回傳
    for index, record in enumerate(record_queue):
        if record.domain_name == domain_name:
            print('find the record from local server')
            counter[index] = count # LRU
            count += 1
            return record.ip_address

    # 沒有的話，就問 root server
    clientSocket.send(domain_name.encode())
    response = clientSocket.recv(1024).decode()

    if response != 'not found': 
        # # FIFO
        # record_queue[victom].domain_name = domain_name
        # record_queue[victom].ip_address = response
        # victom = (victom + 1) % 5

        # LRU
        index = index_replace()
        record_queue[index].domain_name = domain_name
        record_queue[index].ip_address = response
        counter[index] = count
        count += 1
        with open('local_DNS_data.json', 'w') as f:
            json.dump([r.__dict__ for r in record_queue], f, indent=2)
    return response

# 連線設定(對 host 端)
serverPort = 12000
serverHost = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(1)
print('已建立連線')

# 連線設定(對 root 端)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 13000))


# 接收 host server 的 input string
connectionSocket, addr = serverSocket.accept()

while True:
    cmd = connectionSocket.recv(1024).decode()
    print(cmd)

    # 關閉連線
    if cmd == 'close':
        clientSocket.send('close'.encode())
        with open('FIFO.json', 'w') as f:
            json.dump(victom, f)
        with open('LRU.json', 'w') as f:
            json.dump(counter.tolist(), f)
        break

    # 印出當前 FIFO 與 LRU 狀況
    elif cmd == 'print':
        print('-----')
        for index, item in enumerate(record_queue):
            print(item.domain_name, item.ip_address, counter[index])
        print('victom:', victom)
        print('-----')
        connectionSocket.send('print finish'.encode())

    # 將 FIFO 跟 LRU 的值重設
    elif cmd == 'init':
        victom = 0
        counter = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        count = 5.0
        connectionSocket.send('init finish'.encode())
    # 回傳查詢結果
    else:
        result = get_ip(cmd)
        print(result)
        connectionSocket.send(result.encode())


connectionSocket.close()