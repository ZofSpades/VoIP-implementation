import socket
import ssl
import threading
import tkinter as tk

PORT = 12345
CHUNK = 1024

clients = []
client_addresses = []
server_socket = None
running = False

valid_credentials = {
    "user1": "password1",
    "user2": "password2",
    "admin": "admin123"
}

def handle_client(client_socket, client_address):
    try:
        client_socket.sendall(b"Enter username: ")
        username = client_socket.recv(CHUNK).decode().strip()
        client_socket.sendall(b"Enter password: ")
        password = client_socket.recv(CHUNK).decode().strip()

        if username in valid_credentials and valid_credentials[username] == password:
            client_socket.sendall(b"Authentication successful. You are connected.\n")
            clients.append(client_socket)
            client_addresses.append(client_address)
            update_client_list()
            print(f"[INFO] {username} authenticated from {client_address}")
        else:
            client_socket.sendall(b"Authentication failed. Disconnecting.\n")
            client_socket.close()
            return

        while True:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_address in client_addresses:
            client_addresses.remove(client_address)
        update_client_list()
        client_socket.close()

def start_server(button, ip_label):
    global server_socket, running
    if running:
        stop_server(button)
        return
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="ssl/server.crt", keyfile="ssl/server.key")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', PORT))
        server_socket.listen(50)
        server_socket = context.wrap_socket(server_socket, server_side=True)
        running = True
        button.config(text="Stop", bg="#f44336", command=lambda: stop_server(button))
        ip_label.config(text=f"Server IP: {socket.gethostbyname(socket.gethostname())}")
        threading.Thread(target=accept_clients, daemon=True).start()
    except Exception as e:
        print(f"[ERROR] {e}")

def accept_clients():
    global server_socket, running
    while running:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"[INFO] New connection from {client_address}")
            threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
        except Exception:
            break

def stop_server(button):
    global server_socket, running
    if not running:
        return
    running = False
    if server_socket:
        server_socket.close()
    for client in clients:
        client.close()
    clients.clear()
    client_addresses.clear()
    update_client_list()
    button.config(text="Start", bg="#4CAF50", command=lambda: start_server(button, ip_label))

def update_client_list():
    client_list_label.config(text="Connected Clients:\n" + "\n".join([f"{addr[0]}:{addr[1]}" for addr in client_addresses]))

def setup_gui():
    root = tk.Tk()
    root.title("VoIP Server")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    global ip_label, client_list_label
    ip_label = tk.Label(root, text="Server IP: Not Started", font=("Arial", 12), bg="#f0f0f0")
    ip_label.pack(pady=10)

    start_btn = tk.Button(root, text="Start", font=("Arial", 12), bg="#4CAF50", fg="white",
                          command=lambda: start_server(start_btn, ip_label))
    start_btn.pack(pady=10)

    client_list_label = tk.Label(root, text="Connected Clients:\nNone", font=("Arial", 12), bg="#f0f0f0", justify="left")
    client_list_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()