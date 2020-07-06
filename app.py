from wsgiref.simple_server import make_server
from web import App
if __name__ == '__main__':
    addrs = '127.0.0.1'
    port = 9999
    server = make_server(addrs, port, App())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
