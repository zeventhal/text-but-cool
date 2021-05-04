import socket
import threading

HEADER = 64
PORT = 5050
SERVER = '192.168.1.4'
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users = []
usernames = {}

def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")

	connected = True
	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				connected = False
				users.pop(usernames[(addr)])
			print(f"[{addr}] {msg}")
			if msg and msg != DISCONNECT_MESSAGE:
				for i,j in users:
					if i != conn and j != addr:
						i.send((f">>> {msg}").encode(FORMAT))
	conn.close()

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		usernames[(addr)] = len(users)
		users.append((conn, addr))
		print(usernames)
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()