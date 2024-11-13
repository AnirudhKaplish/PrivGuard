import socket
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

with open("vpn_key.key", "wb") as key_file:
    key_file.write(key)

print(f"VPN Server started with encryption key: {key.decode()}")

def start_vpn_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("Listening for client connections...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        encrypted_data = client_socket.recv(4096)

        if encrypted_data:
            try:
                data = cipher.decrypt(encrypted_data).decode()
                print(f"Received (decrypted): {data}")

                response = f"{data}"
                encrypted_response = cipher.encrypt(response.encode())
                client_socket.send(encrypted_response)
            except Exception as e:
                print(f"Error decrypting data: {e}")

        client_socket.close()

if __name__ == "__main__":
    start_vpn_server()
