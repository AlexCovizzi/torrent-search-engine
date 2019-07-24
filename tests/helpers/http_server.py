import http.server
import socketserver
import threading
import os
import time


class HTTPServer:

    def __init__(self):
        self._server = None
        self._thread = None

    def serve(self, host, port, content="", timeout=None):

        class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
            def _set_headers(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            def do_GET(self):
                if timeout is not None:
                    time.sleep(timeout)
                self._set_headers()
                self.wfile.write(content.encode("utf-8"))

        Handler = MyRequestHandler

        self._server = socketserver.TCPServer((host, port), Handler)
        self._thread = threading.Thread(target = self._server.serve_forever)
        self._thread.daemon = True
        self._thread.start()

        return self

    def shutdown(self):
        if self._server:
            self._server.shutdown()
        if self._thread:
            self._thread.join()
