from socket import *
serverPort = 80
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(2)
print("socket aberto")
userNumber = 0
users = []

with open("usuarios.html", "w") as f: #reinicia os usuarios cadastrados
    f.write("<body>\n")
    f.write("    <h1>Usuarios cadastrados</h1>\n")
    f.write("    <p>Nenhum usuario cadastrado</p>\n")
    f.write('    <a href="/index.html">voltar para index</a>\n')
    f.write("</body>")

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
    
    headers, body = receber_request(clientSocket)

    if not headers:
        clientSocket.close()
        continue

    request_line = headers.split("\r\n")[0] #request_line é a primeira linha da requisição
    method, path, version = request_line.split(" ") #GET/POST | O CAMINHO DO ARQUIVO QUE PEDE | VERSAO HTTP
    
    if method == "GET":
        resposta = resposta_get(path)
        clientSocket.send(resposta)
           
    elif method == "POST":
        body = body.decode()
        pares = body.split('&')
        nome = pares[0].split('=')[1]
        idade = pares[1].split('=')[1]
        users.append({"name": nome, "age": idade})  #corta o POST para pegar o nome e idade e salva em uma lista de usuarios
        print(f"Resposta POST tratado: Nome = {users[userNumber]['name']} Idade = {users[userNumber]['age']}")
        resposta_body = f"""
        <html>
            <body>
                <h1>POST recebido</h1>
                <p>POST: Nome = {users[userNumber]['name']} | Idade = {users[userNumber]['age']}</p>
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
        with open("usuarios.html", "w") as f: #atualiza a pagina de usuarios cadastrados
            f.write("<body>\n")
            f.write("    <h1>Usuarios cadastrados</h1>\n")
            for i in range(userNumber+1):
                f.write(f"    <p>Usuario {i}: Nome = {users[i]['name']} | Idade = {users[i]['age']}</p>\n")
            f.write('    <a href="/index.html">voltar para index</a>\n')
            f.write("</body>")

        userNumber += 1
        clientSocket.send(resposta)
        
    clientSocket.close()
