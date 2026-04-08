#!/usr/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler

class ServeurHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.end_headers()

HTTPServer(('',5000),ServeurHTTP).serve_forever()
