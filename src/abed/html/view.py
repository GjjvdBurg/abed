"""
This starts up a simple http server and launches the browser

"""

import os
import SimpleHTTPServer
import SocketServer
import webbrowser

from abed import settings

def view_html():
    port = settings.HTML_PORT
    os.chdir('%s%s%s' % (settings.OUTPUT_DIR, os.sep, 'html'))
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', port), handler)
    webbrowser.open('http://localhost:%i' % port, autoraise=True)
    httpd.serve_forever()

