from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import socket

app = Flask(__name__)

with open("vpn_key.key", "rb") as key_file:
    key = key_file.read()
cipher = Fernet(key)

VPN_SERVER_IP = '127.0.0.1'
VPN_SERVER_PORT = 8080

@app.route('/')
def index():
    return render_template('index.html', key=key.decode(), ip=VPN_SERVER_IP)

@app.route('/send', methods=['POST'])
def send_data():
    data = request.json.get('data')
    encrypted_data = cipher.encrypt(data.encode())

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((VPN_SERVER_IP, VPN_SERVER_PORT))
    client_socket.send(encrypted_data)
    
    encrypted_response = client_socket.recv(4096)
    response = cipher.decrypt(encrypted_response).decode()
    client_socket.close()
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
