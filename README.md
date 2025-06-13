# 🗣️ VoIP Implementation

A simple Voice-over-IP (VoIP) system implemented in Python using raw socket programming and audio streaming. This project contains three variations (types) showcasing progressive implementations of VoIP functionality—starting from basic transmission to full-duplex communication, with added security layers using SSL and user authentication.

---

## 📁 Repository Structure

```
VoIP-implementation-main/
├── ssl/                            # SSL certificate and key storage
│   ├── server.crt                  # Self-signed certificate
│   └── server.key                  # Private key
├── type0/
│   └── full_duplex.py              # Basic full-duplex socket-based audio chat
├── type1/
│   ├── client.py                   # VoIP client with SSL certificate authentication
│   └── server.py                   # VoIP server with SSL certificate authentication
├── type2/
│   ├── client.py                   # VoIP client with SSL and login authentication
│   └── server.py                   # VoIP server with SSL and login authentication
├── LICENSE
```

---

## 🔐 SSL Certificate Setup

To enable SSL encryption and authentication, generate a self-signed certificate:

```bash
# Create a directory to store SSL files
mkdir ssl

# Generate certificate and private key (valid for 365 days)
openssl req -new -x509 -days 365 -nodes -out ssl/server.crt -keyout ssl/server.key
```

Place the generated `server.crt` and `server.key` in the `ssl/` directory.

---

## 🔧 Requirements

- Python 3.x
- `pyaudio` (for real-time audio input/output)
- `socket`, `ssl` (standard library)

Install dependencies:
```bash
pip install pyaudio
```

For Linux users:
```bash
sudo apt-get install portaudio19-dev
```

---

## 🚀 Running the Project

### ▶️ Type 0 – Full Duplex (Unsecured)
Basic socket-based audio chat with bidirectional transmission.

```bash
# Terminal 1 (Server)
python3 type0/full_duplex.py

# Terminal 2 (Client)
python3 type0/full_duplex.py
```

### ▶️ Type 1 – SSL Certificate-Based Authentication
Clients can only connect to the server if they trust the server’s certificate.

```bash
# Terminal 1 (Server)
python3 type1/server.py

# Terminal 2 (Client)
python3 type1/client.py 
```

### ▶️ Type 2 – SSL + Login Authentication
In addition to the SSL certificate, users must log in with a valid username and password.

```bash
# Terminal 1 (Server)
python3 type2/server.py

# Terminal 2 (Client)
python3 type2/client.py
```

---

## 🔐 Security by Type

| Type     | Security Mechanism                              |
|----------|--------------------------------------------------|
| **type0**| No security (plain socket communication)         |
| **type1**| SSL certificate authentication (no login)        |
| **type2**| SSL certificate + username/password authentication |

---

## 🧪 Testing

To test the implementation:

- Run each type on two systems in the same network.
- Use the appropriate `<server_ip>`
- Ensure `ssl/server.crt` and `ssl/server.key` exist when using Type 1 or Type 2.

---

## 📄 License

This project is licensed under the terms of the [MIT License](./LICENSE).

---

## 🙌 Credits

Developed by [ZofSpades](https://github.com/ZofSpades)
