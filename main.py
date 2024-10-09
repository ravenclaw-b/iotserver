import socketserver
import bamdadweb

PORT = 9999
DATA_DIR = "data"

with socketserver.TCPServer(("", PORT), lambda *args: bamdadweb.WebServerHandler(*args, data_dir=DATA_DIR)) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
