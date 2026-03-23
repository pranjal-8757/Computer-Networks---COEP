import socket

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect(("127.0.0.1", 8080))

# HTTP GET request
http_request = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "\r\n"
)

# Send request
client_socket.sendall(http_request.encode())

# Receive response
response = client_socket.recv(4096).decode()

print("HTTP Response received:")
print(response)

# Close socket
client_socket.close()

