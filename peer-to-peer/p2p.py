import socket
import threading

connected_peers = {}
user_name = ""

# Function to continuously receive messages
def receive_messages(connection):
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                print(message)
        except:
            break


# Function to handle newly joined peer
def handle_peer(connection):
    peer_username = connection.recv(1024).decode()
    connected_peers[peer_username] = connection
    connection.send(user_name.encode())
    print(f"{peer_username} has joined..")

    threading.Thread(
        target=receive_messages,
        args=(connection,),
        daemon=True
    ).start()


# Start server to accept incoming peer connections
def launch_server(port_number):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port_number))
    server.listen(5)

    print(f"Server started on port {port_number}")

    while True:
        conn, address = server.accept()
        threading.Thread(
            target=handle_peer,
            args=(conn,),
            daemon=True
        ).start()


# Connect to another peer
def connect_to_peer(ip_address, port_number):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port_number))

        client_socket.send(user_name.encode())
        peer_username = client_socket.recv(1024).decode()

        connected_peers[peer_username] = client_socket
        print(f"Successfully connected with {peer_username}")

        threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        ).start()

    except:
        print("Connection failed")


# Display active peer list
def show_peers():
    if not connected_peers:
        print("No peers connected")
    else:
        print("Active connections:")
        for peer in connected_peers:
            print(peer)


# Messaging interface
def messaging_mode():
    while True:
        show_peers()
        selected_peer = input("Choose peer name (q to quit): ")

        if selected_peer == "q":
            break

        if selected_peer not in connected_peers:
            print("Peer not found")
            continue

        text = input("Enter message: ")
        final_message = f"{user_name}: {text}"
        print(final_message)

        try:
            connected_peers[selected_peer].send(final_message.encode())
        except:
            pass


# ---- Main Execution ----

user_name = input("Mention your username: ")
port_input = int(input("Enter port number: "))

threading.Thread(
    target=launch_server,
    args=(port_input,),
    daemon=True
).start()

while True:
    choice = input("Do you want to connect to another peer? (y/n): ").lower()

    if choice == "y":
        peer_ip = input("Enter peer IP address: ")
        peer_port = int(input("Enter peer Port number: "))
        connect_to_peer(peer_ip, peer_port)

    elif choice == "n":
        break

print("Private messaging mode enabled")
messaging_mode()
