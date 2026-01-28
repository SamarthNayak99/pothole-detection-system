"""
HTTPS Server for Mobile Camera/GPS Access
Uses Python's built-in ssl module
"""
import http.server
import ssl
import socket

# Get local IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Server configuration
PORT = 5500
server_address = ('0.0.0.0', PORT)

# Create HTTP server
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create SSL context (self-signed)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Generate adhoc certificate
try:
    import tempfile
    import subprocess
    
    # Create temporary certificate
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as cert_file:
        cert_path = cert_file.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as key_file:
        key_path = key_file.name
    
    # Generate certificate using openssl
    subprocess.run([
        'openssl', 'req', '-new', '-x509', '-days', '365',
        '-nodes', '-out', cert_path, '-keyout', key_path,
        '-subj', '/CN=localhost'
    ], check=True, capture_output=True)
    
    context.load_cert_chain(cert_path, key_path)
    
except Exception as e:
    print(f"⚠️  Could not generate certificate: {e}")
    print("📝 Please install OpenSSL or use alternative method")
    exit(1)

# Wrap socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"""
╔════════════════════════════════════════════════════════╗
║          🔒 HTTPS SERVER STARTED                       ║
╚════════════════════════════════════════════════════════╝

📱 On your phone, open Chrome and go to:

   https://{local_ip}:5500/home.html

⚠️  IMPORTANT: You will see a security warning!
   
   1. Click "Advanced"
   2. Click "Proceed to {local_ip} (unsafe)"
   
   This is normal for self-signed certificates.

✅ After accepting, camera and GPS will work!

Press Ctrl+C to stop the server
""")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n🛑 Server stopped")
