import socket
from cryptography.fernet import Fernet

# Use the same encryption key as the server
key = b'QyCxrNDYMLmLzY8eLB3CuY9A-lDfVa-9V8sCviG4UZU='  
cipher = Fernet(key)

# Create a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.18.3', 8080))  

# Encrypt and send data
# Encrypt and send data
data = "Hello from client"
encrypted_data = cipher.encrypt(data.encode())
client.send(encrypted_data)

# Receive and decrypt server response
encrypted_response = client.recv(4096)
response = cipher.decrypt(encrypted_response)

print(f"Server response (decrypted): {response.decode()}")

client.close()
