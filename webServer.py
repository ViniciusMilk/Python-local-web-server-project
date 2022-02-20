
# * Importações necessárias
import os
from socket import*

# * Função verifica se o arquivo solicitado exite no servidor e retorna um dicionário com uma chave do tipo booleano, que servirá para manda a resposta correta para o Browser e um valor que é uma string com o nome do arquivo solicitado pelo cliente *#
def search_File(request: str) -> dict:
    request = request.split('/')
    request = request[1].split(' ')
    request = request[0]
    #! Repare que no argumento da função "isfile" passamos o caminho do arquivo desde a raiz concatenado com o arquivo nome do arquivo requisitado
    #* No meu exemplo o caminho era /home/leite/Desktop/HD/linux/Documents/SUPEIOR/REDES-COMPUTADORES/HTTP/
    if os.path.isfile('Caminho do arquivo desde o diretório raiz'+request):
        request = {True: request}
        return request
    else:
        request = {False: request}
        return request

# * Envia a resposta para o cliente
def send_Response(clientsocket: 'socket.socket', request: dict):
    # * Se a chave "True" existir nas chaves do dicionário, a resposta enviada para o cliente será a página solicitada
    if request.get(True):
        #! Repare que no primeiro argumento da funçao "open", passamos o caminho do arquivo concatenado com o nome do arquivo requisitado
        # * No meu exemplo, o caminho era "./HTTP/"
        html = open('Caminho do arquivo/'+request.get(True), 'r')
        html.seek(0, 0)
        file = ''
        for line in html:
            file += line
        # * Montagem do cabeçalho de resposta
        data = "HTTP/1.1 200 OK\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "\r\n"
        data += file
        # * Enviando o cabeçalho codificado para o cliente
        clientsocket.sendall(data.encode())
        clientsocket.shutdown(SHUT_WR)
    # * Caso a chave "True" não exista no dicionário, então a resposta será a página de erro404.html
    else:
        #! Repare agora que no primeiro argumento da funçao "open", passamos o caminho junto nome do arquivo erro404.html
        # * No meu exemplo, o caminho era "./HTTP/"
        erro = open('Caminho do arquivo/erro404.html', 'r')
        erro.seek(0, 0)
        file = ''
        for line in erro:
            file += line
        # * Montagem do cabeçalho de resposta
        data = "HTTP/1.1 404 Not Found\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "\r\n"
        data += file
        # * Enviando o cabeçalho codificado para o cliente
        clientsocket.sendall(data.encode())
        clientsocket.shutdown(SHUT_WR)

#! Cria o servidor web
def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('localhost', 8080))
        serversocket.listen(5)
        print('Servidor Web aguardando requisição')
        while (1):
            (clientsocket, Address) = serversocket.accept()

            request = clientsocket.recv(5000).decode()
            request = request.split("\n")
            print(request[0])
            request = search_File(request[0])
            send_Response(clientsocket, request)

    except KeyboardInterrupt:
        print("\nDesligando Servidor Web...\n")
        serversocket.close()


print('Access http://localhost:8080')
#* Chamada da funca createServer()
createServer()
