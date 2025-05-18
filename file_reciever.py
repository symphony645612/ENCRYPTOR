import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = b'ThisIsA16ByteKey'  # Must be 16, 24, or 32 bytes
iv = b'ThisIsAnInitVectr'  # 16 bytes

host = '0.0.0.0'  # Listen on all interfaces
port = 5001

s = socket.socket()
s.bind((host, port))
s.listen(1)
print(f"[+] Listening on port {port}...")

conn, addr = s.accept()
print(f"[+] Connection from {addr}")

# Receive the encrypted file data
filename = conn.recv(1024).decode()
print(f"[+] Receiving file: {filename}")
conn.send(b'FILENAME RECEIVED')

with open("received_encrypted_file", 'wb') as f:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)

conn.close()
s.close()

# Decrypt the file
with open("received_encrypted_file", 'rb') as f:
    encrypted_data = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

with open(f"decrypted_{filename}", 'wb') as f:
    f.write(decrypted_data)

print(f"[+] File received and decrypted as decrypted_{filename}")
