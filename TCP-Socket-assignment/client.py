import socket

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client socket initialized")

client_socket.connect(("127.0.0.1", 8000))

print("Connected to server")

while True:
    client_message = input("Client: ")

    client_socket.send(client_message.encode())

    if client_message.lower() == "exit":
        break

    server_reply = client_socket.recv(1024).decode()

    if not server_reply:
        print("Server disconnected")
        break

    print("Server:", server_reply)

# Close socket
client_socket.close()
print("Connection closed by client")

