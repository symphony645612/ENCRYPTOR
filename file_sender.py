import socket
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# ==== SETTINGS ====
receiver_ip = '192.168.1.12'  # <-- Change to receiver's IP
port = 5001
filename = 'friends.DNG'  # <-- Change to your file
password = input("Enter password to encrypt the file: ")

# ==== FILE ENCRYPTION ====
salt = get_random_bytes(16)  # Unique salt
key = PBKDF2(password, salt, dkLen=32, count=100000)  # AES-256 key
iv = get_random_bytes(16)  # AES requires 16-byte IV

# Read and encrypt the file
with open(filename, 'rb') as f:
    file_data = f.read()

cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))

# ==== SEND OVER SOCKET ====
s = socket.socket()
s.connect((receiver_ip, port))

# Send file name
s.send(filename.encode())
ack = s.recv(1024)
if ack != b'FILENAME RECEIVED':
    print("[-] Failed to sync.")
    s.close()
    exit()

# Send salt and IV
s.send(salt)
s.recv(2)
s.send(iv)
s.recv(2)

# Send encrypted file
s.sendall(encrypted_data)
s.close()
print("[+] File encrypted and sent.")
