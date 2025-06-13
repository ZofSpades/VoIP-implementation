import socket
import threading
import tkinter as tk
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 12345

audio = pyaudio.PyAudio()
local_ip = socket.gethostbyname(socket.gethostname())

send_thread = None
receive_thread = None
send_sock = None
receive_sock = None
running = False

def send_audio(target_ip):
    global send_sock, running
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    running = True
    try:
        print(f"Sending audio to {target_ip}:{PORT}...")
        while running:
            frame = stream.read(CHUNK)
            send_sock.sendto(frame, (target_ip, PORT))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        stream.stop_stream()
        stream.close()
        send_sock.close()

def receive_audio():
    global receive_sock, running
    receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_sock.bind(('0.0.0.0', PORT))
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
    try:
        print(f"Listening on port {PORT}...")
        while running:
            data, _ = receive_sock.recvfrom(4096)
            stream.write(data)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        stream.stop_stream()
        stream.close()
        receive_sock.close()

def start_voip(target_ip, button):
    global send_thread, receive_thread, running
    if running:
        stop_voip(button)
        return
    if not target_ip:
        print("[ERROR] Please enter a valid IP address")
        return
    try:
        socket.inet_aton(target_ip)
    except socket.error:
        print("[ERROR] Invalid IP address format")
        return
    running = True
    send_thread = threading.Thread(target=send_audio, args=(target_ip,), daemon=True)
    receive_thread = threading.Thread(target=receive_audio, daemon=True)
    send_thread.start()
    receive_thread.start()
    button.config(text="Stop", bg="#f44336", command=lambda: stop_voip(button))
    print("[INFO] VoIP started")

def stop_voip(button):
    global running
    if not running:
        return
    running = False
    if send_sock:
        send_sock.close()
    if receive_sock:
        receive_sock.close()
    button.config(text="Connect", bg="#4CAF50", command=lambda: start_voip(target_ip_entry.get(), button))
    print("[INFO] VoIP stopped")

def setup_gui():
    root = tk.Tk()
    root.title("VoIP Chat")
    root.geometry("400x250")
    root.configure(bg="#f0f0f0")
    tk.Label(root, text=f"Your IP Address: {local_ip}", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
    tk.Label(root, text="Enter Target IP:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    global target_ip_entry
    target_ip_entry = tk.Entry(root, font=("Arial", 12), justify="center")
    target_ip_entry.pack(pady=5)
    connect_btn = tk.Button(root, text="Connect", font=("Arial", 12), bg="#4CAF50", fg="white",
                            command=lambda: start_voip(target_ip_entry.get(), connect_btn))
    connect_btn.pack(pady=5)
    root.mainloop()

if __name__ == "__main__":
    setup_gui()