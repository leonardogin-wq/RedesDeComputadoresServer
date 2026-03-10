from socket import *
serverPort = 8103
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(2)
print("socket aberto")
ip, porta = serverSocket.accept()
print("conectado")

def resposta_get(path): #resposta pro web browser
    if path == "/":
        path = "index.html"
    else:
        path = path[1:] # Remove a barra inicial
    ArquivoRequerido = open(path, "r").read()
    resposta = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(ArquivoRequerido.encode())}\r\n"
                "\r\n"
                + ArquivoRequerido)
    return resposta.encode()

while 1:
    request = ip.recv(4096).decode()
    if request:
        print(request)
        request_line = request.split("\r\n")[0] #request_line é a primeira linha da requisição
        method, path, version = request_line.split(" ") #GET/POST | O CAMINHO DO ARQUIVO QUE PEDE | VERSAO HTTP
    if method == "GET":
        resposta = resposta_get(path)
        ip.send(resposta.encode())
           
    if method == "POST":
        print("é post")

    
