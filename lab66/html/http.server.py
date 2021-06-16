import sys
import time
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

ip = "127.0.0.1"
port = 8000
url = "http://127.0.0.1:8000"


def start_server():
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


threading.Thread(target=start_server).start()
webbrowser.open_new(url)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)