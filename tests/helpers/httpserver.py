import http.server
import socketserver
import threading
import os
import time


class httpserver:

    def __init__(self, host, port, content="", timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.content = content
        self._server = None
        self._thread = None

    def serve(self):
        this = self

        class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
            def _set_headers(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            def do_GET(self):
                if this.timeout is not None:
                    time.sleep(this.timeout)
                self._set_headers()
                self.wfile.write(this.content.encode("utf-8"))

        Handler = MyRequestHandler

        self._server = socketserver.TCPServer((self.host, self.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever)
        self._thread.daemon = True
        self._thread.start()

        return self

    def shutdown(self):
        if self._server:
            self._server.shutdown()
        if self._thread:
            self._thread.join()

    def __enter__(self):
        return self.serve()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._server.shutdown()
        return False
