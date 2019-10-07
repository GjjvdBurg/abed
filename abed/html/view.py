"""
This starts up a simple http server and launches the browser

"""

import errno
import os
import webbrowser

from six.moves import SimpleHTTPServer, socketserver

from socket import error as socket_error

from ..conf import settings
from ..io import warning


def view_html():
    port = settings.HTML_PORT
    os.chdir("%s%s%s" % (settings.OUTPUT_DIR, os.sep, "html"))
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    while True:
        try:
            httpd = socketserver.TCPServer(("", port), handler)
            break
        except socket_error as err:
            if not err.errno == errno.EADDRINUSE:
                raise err
            warning("Port already in use, trying %i" % (port + 1))
            port += 1

    webbrowser.open("http://localhost:%i" % port, autoraise=True)
    httpd.serve_forever()
