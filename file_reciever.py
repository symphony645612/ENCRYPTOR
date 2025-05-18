import socket
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad

# ==== SETTINGS ====
host = '0.0.0.0'
port = 5001

# ==== RECEIVE FILE ====
s = socket.socket()
s.bind((host, port))
s.listen(1)
print(f"[+] Listening on port {port}...")

conn, addr = s.accept()
print(f"[+] Connection from {addr}")

filename = conn.recv(1024).decode()
print(f"[+] Receiving file: {filename}")
conn.send(b'FILENAME RECEIVED')

# Receive salt
salt = conn.recv(16)
conn.send(b'ok')

# Receive IV
iv = conn.recv(16)
conn.send(b'ok')

# Receive encrypted data
with open("received_encrypted_file", 'wb') as f:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)
conn.close()
s.close()

# ==== DECRYPT ====
password = input("Enter password to decrypt the file: ")
key = PBKDF2(password, salt, dkLen=32, count=100000)

with open("received_encrypted_file", 'rb') as f:
    encrypted_data = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    with open(f'decrypted_{filename}', 'wb') as f:
        f.write(decrypted_data)
    print(f"[+] File decrypted as: decrypted_{filename}")
except ValueError:
    print("[-] Wrong password or corrupted data.")
