#!/usr/bin/env python

'''

Jay's webserver

$ python jayweb.py
serving on port 8080
method=GET
headers=User-Agent: curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 OpenSSL/0.9.8z zlib/1.2.5
Host: localhost:8080
Accept: */*

path=/asdf
query string={'asdf': ['sd']}

and the request using curl

$ curl -v http://localhost:8080/asdf?asdf=sd
* About to connect() to localhost port 8080 (#0)
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /asdf?asdf=sd HTTP/1.1
> User-Agent: curl/7.21.4 (universal-apple-darwin11.0) libcurl/7.21.4 OpenSSL/0.9.8z zlib/1.2.5
> Host: localhost:8080
> Accept: */*
> 
< HTTP/1.1 200 OK
< Content-Length: 32
< 
* Connection #0 to host localhost left intact
* Closing connection #0
<html><body>Hi Jay</body></html>

'''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import httplib
import urlparse

class _web(BaseHTTPRequestHandler):

    # Liam's stupid object holder
    class objContainer:
        def __init__(self):
            pass

    def __class__(self):
        pass

    def do_GET(self):

        _objContainer = self.objContainer()

        _objContainer.method = "GET"
        _objContainer.headers = self.headers
        _objContainer.path = urlparse.urlparse(self.path)
        _objContainer.qs = urlparse.parse_qs(_objContainer.path.query)

        print "method=%s" % (_objContainer.method)
        print "headers=%s" % (_objContainer.headers)
        print "path=%s" % (_objContainer.path.path)
        print "query string=%s" % (_objContainer.qs)

        self.protocol_version = "HTTP/1.1"
        self.send_response(httplib.OK)
        _body = """<html><body>Hi Jay</body></html>"""
        self.send_header('Content-Length',str(len(_body)))
        self.end_headers()
        self.wfile.write(_body)

    def send_response(self,code,message=None):
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" % (self.protocol_version, code, message))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

if __name__ == '__main__':
    listen_port = 8080
    print "serving on port %s" % (listen_port)
    httpd = ThreadedHTTPServer(('', listen_port), _web)
    httpd.serve_forever()
