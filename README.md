# 次世代無線網路概論
## Assignment1
In this programming assignment, we will write a socket program to build a simple client-server system.

### I. Basic requirements (70%)
* Connection and communication: (30%) Establish TCP connections between clients and a server to send and receive messages.
* Simple program operation: (30%)
```
Client: Input three parameters as triangle sides to inquire the server which kind of triangle it is?
Server: Confirm request from clients and respond to the answer
Ex. acute triangle, obtuse triangle, right triangle, or not a triangle
```
* Read file: (10%)
Use text file , Ex. 3,4,5 SPO 
### II. Advanced requirements (30%)
* Identity Verification: (20%)
```
Client: Input account and password
Ex. B12345678:AB12 LOGIN
Server: Check identity of clients
1) Reply “Valid” for a successful login, then execute simple program operation.
2) Otherwise, reply “Invalid” and make a “Permission Denied” response if clients try to execute the simple program operation.
```
* Encryption: (10%)
```
Preprocess: Encrypt plaintext of the password in the text file with shift-two method (Caesar shift cypher)
Server: Decrypt cyphertext of the password in the text file with shift-two method (Caesar shift cypher)
```

## Assignment2
In this programming assignment, we will simulate the operation of the DNS system.

* Basic Request Response(40%)
```
Establish TCP connections between service server and local DNS server.
Service server will send domain name to DNS server and DNS server will response corresponding IP address or “not found” to service server.
```
* Recursive DNS(40%)
```
Construct another DNS server as root DNS server.
If local DNS server didn’t have corresponding IP address, local DNS server should ask root DNS server.
If root DNS server do have the corresponding IP address for domain name, local DNS server should record the response and return the IP address to service server.
```
* Resource Record —— CNAME(10%)

A type of resource record in the DNS that maps one domain name (an alias) to another (the canonical name).

* Capacity Problem(10%)
```
Consider local DNS server can only save 5 records as a queue and root DNS server have 10 records.
If the queue is full, you should pop out the last record of local DNS server while the records have been updated.
```
* Bonus-LRU replacement(15%)

Local DNS server uses LRU(least recently used) replacement to refresh the records.
