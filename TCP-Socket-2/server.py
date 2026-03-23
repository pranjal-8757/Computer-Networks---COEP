import socket

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to IP and port
server_socket.bind(("127.0.0.1", 8080))

# Listen for connections
server_socket.listen(1)
print("HTTP Server running on port 8080...")

while True:
    connection, address = server_socket.accept()
    print("Client connected from:", address)

    # Receive HTTP request
    request = connection.recv(1024).decode()
    print("HTTP Request received:")
    print(request)

    # HTTP response body
    html_content = """
    <html>
        <head><title>Simple HTTP Server</title></head>
        <body>
            <h1>HTTP Server using TCP Sockets</h1>
            <p>This response is sent from a Python server.</p>
        </body>
    </html>
    """

    # HTTP response
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "\r\n"
        + html_content
    )

    # Send response
    connection.sendall(response.encode())

    # Close connection
    connection.close()
    print("Connection closed\n")

