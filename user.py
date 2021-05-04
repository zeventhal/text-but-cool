import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.1.4'
ADDR = (SERVER, PORT)
connected = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)

def rec():
	while connected:
		print(client.recv(2048).decode(FORMAT))

# a new thread for message recieving
thread = threading.Thread(target=rec, args=())
thread.start()

while True:
	sms = input('')
	send(sms)
	if sms == DISCONNECT_MESSAGE:
		connected = False
		break
