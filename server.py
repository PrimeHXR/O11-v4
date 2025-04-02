import os
import subprocess
import http.server
import socketserver
import ssl
import threading
from http import HTTPStatus
from flask import Flask, request, send_file

HOSTS_PATH = "/etc/hosts"
DOMAIN = "lic.cryptolive.one"
DOMAIN2 = "lic.bitmaster.cc"
IP_ADDRESS = ""
PORT_HTTP = 80
PORT_HTTPS = 443
CERTS_PATH = "./certs"
KEY_FILE = os.path.join(CERTS_PATH, "key.pem")
CERT_FILE = os.path.join(CERTS_PATH, "cert.pem")

app = Flask(__name__)

@app.before_request
def log_request():
    if request.method == 'POST':
        print(f"Received POST request to {request.url}")
        print("Headers:", dict(request.headers))
        try:
            if request.is_json:
                print("Body:", request.get_json())
            elif request.form:
                print("Form data:", request.form.to_dict())
            elif request.data:
                print("Raw data:", request.data.decode('utf-8'))
        except Exception as e:
            print(f"Error parsing request body: {e}")

@app.route('/lic', methods=['POST'])
def handle_lic():
    print("Received POST /lic request")
    
    file_path = os.path.join(os.getcwd(), "lic.cr")
    
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return "File not found", HTTPStatus.NOT_FOUND
    
    if request.form:
        print("Form data:", request.form.to_dict())
    
    return send_file(file_path, as_attachment=True)

@app.route('/')
def index():
    return "Welcome to the license server!"

# Ensure certificates exist
def generate_certificates():
    if not os.path.exists(CERTS_PATH):
        os.makedirs(CERTS_PATH)
    
    if not os.path.exists(KEY_FILE) or not os.path.exists(CERT_FILE):
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", KEY_FILE,
            "-out", CERT_FILE, "-days", "365", "-nodes", "-subj", "/CN=localhost"
        ], check=True)

def update_hosts():
    try:
        with open(HOSTS_PATH, "r+") as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)
            hosts_file.truncate()
            
            # Remove existing domain entries
            lines = [line for line in lines if DOMAIN not in line and DOMAIN2 not in line]
            
            # Append new domain mappings
            lines.append(f"{IP_ADDRESS} {DOMAIN}\n")
            lines.append(f"{IP_ADDRESS} {DOMAIN2}\n")
            
            hosts_file.writelines(lines)
            print(f"Successfully mapped {DOMAIN} to {IP_ADDRESS} in {HOSTS_PATH}")
            print(f"Successfully mapped {DOMAIN2} to {IP_ADDRESS} in {HOSTS_PATH}")
    except Exception as e:
        print(f"Error updating hosts file: {e}")

def run_http_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT_HTTP), handler) as httpd:
        print(f"HTTP server running on port {PORT_HTTP}")
        httpd.serve_forever()

def run_https_server():
    generate_certificates()
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT_HTTPS), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=KEY_FILE, certfile=CERT_FILE, server_side=True)
    print(f"HTTPS server running on port {PORT_HTTPS}")
    httpd.serve_forever()

if __name__ == "__main__":
    update_hosts()
    generate_certificates()
    
    threading.Thread(target=run_http_server, daemon=True).start()
    threading.Thread(target=run_https_server, daemon=True).start()
    
    app.run(host="0.0.0.0", port=5454)
