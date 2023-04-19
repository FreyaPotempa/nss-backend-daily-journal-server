import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_entries, get_single_entry, delete_entry, get_all_moods, get_searched_entry


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        '''parses the url'''

        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)

    def do_GET(self):
        '''handles GET requests to the server'''
        self._set_headers(200)
        response = {}
        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            if id is not None:
                response = get_single_entry(id)
            else:
                response = get_all_entries()

        elif resource == "moods":
            response = get_all_moods()

        print(response)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        pass

    def do_DELETE(self):
        '''delete handler'''
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        '''sets status code, content-type and access-control-allow-origin headers on response

        Args:
            status (number): the status code to return to the front end'''
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
