import socket
import ssl
import threading
import tkinter as tk
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 12345

audio = pyaudio.PyAudio()
running = False
client_socket = None

def send_audio():
    global running, client_socket
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    try:
        while running:
            frame = stream.read(CHUNK)
            client_socket.sendall(frame)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        stream.stop_stream()
        stream.close()

def receive_audio():
    global running, client_socket
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
    try:
        while running:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        stream.stop_stream()
        stream.close()

def start_voip(server_ip, username, password, button):
    global running, client_socket
    if running:
        stop_voip(button)
        return
    if not server_ip or not username or not password:
        print("[ERROR] Please enter all fields")
        return
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations("ssl/server.crt")
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket = context.wrap_socket(raw_socket, server_hostname=server_ip)
        client_socket.connect((server_ip, PORT))
        client_socket.sendall(username.encode() + b"\n")
        client_socket.sendall(password.encode() + b"\n")

        response = client_socket.recv(CHUNK).decode()
        print(response)
        if "Authentication failed" in response:
            client_socket.close()
            return
    except Exception as e:
        print(f"[ERROR] {e}")
        return
    running = True
    threading.Thread(target=send_audio, daemon=True).start()
    threading.Thread(target=receive_audio, daemon=True).start()
    button.config(text="Disconnect", bg="#f44336", command=lambda: stop_voip(button))

def stop_voip(button):
    global running, client_socket
    if not running:
        return
    running = False
    if client_socket:
        client_socket.close()
    button.config(text="Connect", bg="#4CAF50", command=lambda: start_voip(server_ip_entry.get(), username_entry.get(), password_entry.get(), button))

def setup_gui():
    root = tk.Tk()
    root.title("VoIP Chat Client")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")
    tk.Label(root, text="Enter Server IP:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    global server_ip_entry, username_entry, password_entry
    server_ip_entry = tk.Entry(root, font=("Arial", 12), justify="center")
    server_ip_entry.pack(pady=5)
    tk.Label(root, text="Enter Username:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    username_entry = tk.Entry(root, font=("Arial", 12), justify="center")
    username_entry.pack(pady=5)
    tk.Label(root, text="Enter Password:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    password_entry = tk.Entry(root, font=("Arial", 12), justify="center", show="*")
    password_entry.pack(pady=5)
    connect_btn = tk.Button(root, text="Connect", font=("Arial", 12), bg="#4CAF50", fg="white",
                            command=lambda: start_voip(server_ip_entry.get(), username_entry.get(), password_entry.get(), connect_btn))
    connect_btn.pack(pady=5)
    root.mainloop()

if __name__ == "__main__":
    setup_gui()