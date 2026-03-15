import socket

SERVER = "127.0.0.1"
PORT = 1025

sender = "pranjal@mail.com"
recipient = "receiver@mail.com"
subject = "SMTP CN Lab Test"
body = "Hello,\nThis is a test mail.. \n FROM Pranjal"

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    print("Connected to SMTP server\n")

    def send(cmd):
        print("C:", cmd.strip())
        client.sendall(cmd.encode())
        response = client.recv(1024).decode()
        print("S:", response.strip())
        print()

    # Server greeting
    print("S:", client.recv(1024).decode().strip(), "\n")

    send("HELO localhost\r\n")
    send(f"MAIL FROM:<{sender}>\r\n")
    send(f"RCPT TO:<{recipient}>\r\n")
    send("DATA\r\n")

    message = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
    client.sendall(message.encode())
    print("S:", client.recv(1024).decode().strip(), "\n")

    send("QUIT\r\n")

    client.close()

except Exception as e:
    print("Error:", e)

