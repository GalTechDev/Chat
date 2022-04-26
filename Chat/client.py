import socket
import threading
reso = input("Entrer ip: ")
port = int(input("Entrer port: "))
nickname = input("Choisir un Pseudo: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((reso, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK":
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("Une erreur s'est provoqué!")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
