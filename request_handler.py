import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_entries, get_single_entry, delete_entry, get_all_moods, get_searched_entries, create_entry, update_entry


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        '''parses the url'''

        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        '''handles GET requests to the server'''
        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)
        # use query params to get the search term
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                else:
                    response = get_all_entries()

            elif resource == "moods":
                response = get_all_moods()
        else:
            (resource, query) = parsed

            if query.get('q') and resource == "entries":
                response = get_searched_entries(query['q'][0])
                print("response", response)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        '''handles POST requests'''
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        created_entry = None

        if resource == "entries":
            self._set_headers(201)
            created_entry = create_entry(post_body)

        self.wfile.write(json.dumps(created_entry).encode())

    def do_PUT(self):
        '''updates an entry'''

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)

            if success:
                self._set_headers(204)
            else:
                self._set_headers(404)

        self.wfile.write(json.dumps(post_body).encode())

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
