"""
Simple HTTPS server for mobile testing
Generates self-signed certificate automatically
"""
import http.server
import ssl
import os
from pathlib import Path

# Create certificate if it doesn't exist
cert_file = "cert.pem"
key_file = "key.pem"

if not os.path.exists(cert_file) or not os.path.exists(key_file):
    print("🔐 Generating self-signed certificate...")
    os.system(f'openssl req -new -x509 -keyout {key_file} -out {cert_file} -days 365 -nodes -subj "/CN=localhost"')
    print("✅ Certificate generated!")

# Create HTTPS server
server_address = ('0.0.0.0', 5500)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Wrap with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_file, key_file)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

import socket
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"""
✅ HTTPS Server Started!

📱 On your phone, open:
   https://{local_ip}:5500/home.html
   https://10.42.117.136:5500/home.html

⚠️  You'll see a security warning - this is normal!
    Click "Advanced" → "Proceed anyway"

🔒 This enables camera and GPS permissions
""")

httpd.serve_forever()
