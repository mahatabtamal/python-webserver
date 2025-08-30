import os
from http.server import BaseHTTPRequestHandler
from routes.main import routes
# from pathlib import Path

from response.templateHandler import TemplateHandler
from response.badRequestHander import BadRequestHandler

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return
    
    def do_POST(self):
        return
    
    def do_GET(self):
        split_path = os.path.splitext(self.path) # returns the path as tuple
        request_extension = split_path[1]

        # only accept HTML for now and reject anything else
        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })
        
    def handle_http(self, status, content_type):
        """What it does that it sends some 'response' which is an int Code like
        200 and 404 that works as a status of some action in very simple terms.
        Then it sends an HTTP header. The header is a formatted text(key-value
        pair) that provides info about the transmitted data, i.e metadata."""
        status = 200
        content_type = "text/plain"
        response_content = ""

        # routes is a dict that contains paths of files
        if self.path in routes:
            # print it
            print(routes[self.path])
            # the contents are stored in another dict inside routes dict
            route_content = routes[self.path]['template']
            # format it into path. Templates have the HTML files
            filepath = Path("templates/{}".format(route_content))
            # if the file exists, do
            if filepath.is_file():
                content_type = "text/html"
                # open and return it into a stream
                response_content = open("templates/{}".format(route_content))
                # then read it
                response_content = response_content.read()
            # if it doesn't, return 404 error
            else:
                content_type = "text/plain"
                response_content = "404 not found"

        # Then we have responses, the actual data sent back from the server.
        self.send_response(status)
        # sending headers
        self.send_header('Content-type', content_type)
        self.end_headers()

        # grabs stuff from routes/main.py
        route_content = routes[self.path]
        # to confirm that http is working
        return bytes("Hello World", "UTF-8")
    
    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
