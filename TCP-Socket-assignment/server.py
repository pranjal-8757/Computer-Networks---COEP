import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Server socket initialized")

# Bind socket to IP and port
server_socket.bind(("127.0.0.1", 8000))

server_socket.listen(1)
print("Server is listening for connections...")

while True:
    connection, client_address = server_socket.accept()
    print("Client connected from:", client_address)

    while True:
        client_data = connection.recv(1024).decode()

        if not client_data or client_data.lower() == "exit":
            print("Client requested to close connection")
            break

        print("Client:", client_data)

        server_response = input("Server: ")
        connection.send(server_response.encode())

    connection.close()
    print("Client connection terminated")

server_socket.close()

