from socket import *
serverPort = 8108
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(2)
print("socket aberto")

def get_content_type(path):
    if path.endswith(".html"):
        return "text/html"
    elif path.endswith(".jpeg") or path.endswith(".jpg"):
        return "image/jpeg"
    elif path.endswith(".png"):
        return "image/png"
    elif path.endswith(".css"):
        return "text/css"
    elif path.endswith(".js"):
        return "application/octet-stream"
    else:
        return "application/octet-stream"


def resposta_get(path): #resposta pro web browser
    if path == "/":
        path = "index.html"
    else:
        path = path[1:] # Remove a barra inicial
    #ArquivoRequerido = open(path, "r").read()
    try:
        with open(path, "rb") as f:
            conteudo = f.read()
        status = "200 OK"
    except FileNotFoundError:
        conteudo = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"

    content_type = get_content_type(path)

    headers = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(conteudo)}\r\n"
        "\r\n"
        ).encode()
    return headers + conteudo

def receber_request(clientSocket):
    data = b""

    # ler até terminar os headers
    while b"\r\n\r\n" not in data:
        data += clientSocket.recv(1024)
    headers, rest = data.split(b"\r\n\r\n", 1)
    headers_str = headers.decode()

    # pega Content-Length
    content_length = 0
    for line in headers_str.split("\r\n"):
        if "Content-Length" in line:
            content_length = int(line.split(":")[1].strip())
    body = rest

    # lê o restante do body se precisar
    while len(body) < content_length:
        body += clientSocket.recv(1024)
    return headers_str, body



while True:
    clientSocket, addr = serverSocket.accept()
    print("conectado: ", addr)
    
    headers, body = receber_request(clientSocket)
    # duplicados abaixo (REMOVER)
    #request_line = headers.split("\r\n")[0]
    #method, path, version = request_line.split(" ")

    if not headers:
        clientSocket.close()
        continue
    
    print(headers)

    request_line = headers.split("\r\n")[0] #request_line é a primeira linha da requisição
    method, path, version = request_line.split(" ") #GET/POST | O CAMINHO DO ARQUIVO QUE PEDE | VERSAO HTTP
    
    if method == "GET":
        resposta = resposta_get(path)
        clientSocket.send(resposta)
           
    elif method == "POST":
        print("BODY:", body)
        resposta_body = f"""
        <html>
            <body>
                <h1>POST recebido</h1>
                <p>{body.decode()}</p>
                <p>Retornar para formulario: <a href="/post.html">Formulario POST</a></p>
            </body>
        </html>
        """
        resposta = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(resposta_body.encode())}\r\n"
            "\r\n"
            + resposta_body
        ).encode()
        clientSocket.send(resposta)
        
    clientSocket.close()