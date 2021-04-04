#!/usr/bin/env python

import CGIHTTPServer
import BaseHTTPServer

# - - - for local testing - - -

if __name__ == "__main__":
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("", 8001)
    handler.cgi_directories = ["/"]
    httpd = server(server_address, handler)
    httpd.serve_forever()
