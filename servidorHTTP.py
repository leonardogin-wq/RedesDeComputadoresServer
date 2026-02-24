from socket import *
serverPort = 8084
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(2)
print("socket aberto")
ip, porta = serverSocket.accept()
print("conectado")

while 1:
    request = ip.recv(4096).decode()
    if request:
        print(request)
    if request == "/":
        request = "/index.html"
        open("htdocs" + request)
    
