import socket
import threading

# Connection Data
HOST = input("IP : ")
PORT = int(input("PORT: "))
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

###COMMANDS (mettre un point d'exclamation devant)###
STOP_SERVER = 'STOP' # Arret du serveur
KICK_SERVER = 'KICK' # Expulser un joueur
LIST_SERVER = 'LIST' # avoir la liste des joueur connecter
MP_SERVER = 'MP' # envoyer un message privée a un joueur

# Server Initialisation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f'[STARTING]: Server host {HOST} is listening on port {PORT}')

# Clients Info
clients = []
nicknames = []

def broadcast(message):
    print(f'[BROADCAST]: {message.decode(FORMAT)}')
    for client in clients:
        client.send(message)

def kick_all():
    for client in clients:
        client.close()

def handle(client):
    while True:
        try:
            # Broadcasting message
            message = client.recv(1024)
            broadcast(message)
        except:
            #Removing and closing Client
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} left!'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        try:
            # Accept Connection
            client, addr = server.accept()
            print(f'[CLIENT]: Connected with {addr}')

            # Request and Store NickName
            client.send('NICK'.encode(FORMAT))
            nickname = client.recv(1024).decode(FORMAT)
            nicknames.append(nickname)
            clients.append(client)
            print(nicknames)

            #Print and broadcast NickNames
            print(f'[CLIENT]: Nickname is {nickname}')
            broadcast(f'{nickname} joined!'.encode(FORMAT))
            client.send('Connected to the server!'.encode(FORMAT))

            #Start handeling thread from client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            print('[SERVER]: Server has been terminated...')
            break

def promt():
    while True:
        command = input()

        if command[0] == '!':
            command = command[1::]
            command = command.split(' ')
            
            if command[0] == STOP_SERVER:
                broadcast('[SERVER]: shut down...'.encode(FORMAT))
                kick_all()
                server.close()
                break
            
            elif command[0] == LIST_SERVER:
                print(f'[LIST]: {nicknames}')
            
            elif command[0] == KICK_SERVER:
                nick = ''
                try:
                    nick = command[1]
                except IndexError:
                    print('[ERROR]: Uncomplete command')
                
                if len(command) > 2:
                    reason = str([command[i] + ' ' for i in range(2,len(command))])
                else:
                    reason = 'not precised'
                
                try:
                    index = nicknames.index(nick)
                    clients[index].send(f"You will be banned in few seconds for reason : {' '.join(reason)}".encode(FORMAT))
                    clients[index].close()
                except ValueError:
                    print('[ERROR]: Client not found')

            elif command[0] == MP_SERVER:
                nick = ''
                try:
                    nick = command[1]
                except IndexError:
                    print('[ERROR]: Uncomplete command')

                try:
                    message = [command[i] + ' ' for i in range(2,len(command))]
                    
                    try:
                        index = nicknames.index(nick)
                        clients[index].send(f"[ServerMP]: {' '.join(message)}".encode(FORMAT))
                    except ValueError:
                        print('[ERROR]: Client not found')
                    
                except IndexError:
                    print('[ERROR]: Please enter a message to send')

            else:
                print(f"[ERROR]: command was not reconized")
        else:
            broadcast(f'[SERVER]: {command}'.encode(FORMAT))

##START##
r_thread = threading.Thread(target=receive)
promt_thread = threading.Thread(target=promt)

r_thread.start()
promt_thread.start()
