from socket import *
import json

# record 紀錄 ip 跟 domain name
class Record:
    def __init__(self, ip_address, domain_name, canonical_name=None):
        self.ip_address = ip_address
        self.domain_name = domain_name
        if canonical_name == None:
            self.canonical_name = domain_name
record_queue = []

# 讀 json 檔
file = open('root_DNS_data.json')
data = json.load(file)
file.close()
for item in data:
    if item['type'] == 'A':
        record = Record(item['ip_address'], item['domain_name'])
        record_queue.append(record)
for item in data:
    if item['type'] == 'CNAME':
        for r in record_queue:
            if r.domain_name==item['canonical name']:
                r.canonical_name = item['alias']

# for item in record_queue:
#     print(item.ip, item.domain_name, item.canonical_name)

def get_ip(domain_name):
    for record in record_queue:
        if record.domain_name == domain_name or record.canonical_name == domain_name:
            print('find the record from root server')
            return record.ip_address
    return "not found"

serverPort = 13000
serverHost = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(1)

connectionSocket, addr = serverSocket.accept()
while True:
    command = connectionSocket.recv(1024).decode()
    print(command)
    if command == 'close':
        break
    connectionSocket.send(get_ip(command).encode())

connectionSocket.close()