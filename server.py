import socket
from cryptography.fernet import Fernet

# Key generation and encryption setup
key = Fernet.generate_key()
cipher = Fernet(key)

# Create a VPN server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)

print(f"Server started, encryption key: {key.decode()}")

# Handle client connections
while True:
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address}")

    # Receive encrypted data from the client
    encrypted_data = client_socket.recv(4096)
    
    if encrypted_data:
        # Decrypt the data
        data = cipher.decrypt(encrypted_data)
        print(f"Received (decrypted): {data.decode()}")

        # Simulate processing (e.g., forwarding data to a remote server)
        response = f"Server response to: {data.decode()}"
        
        # Encrypt the response and send it back to the client
        encrypted_response = cipher.encrypt(response.encode())
        client_socket.send(encrypted_response)

    client_socket.close()
