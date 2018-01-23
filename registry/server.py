from jie.server import Server, listen 

from controller import registry_bp


server = Server('regisrty')
server.listener = listen(False, False)
server.app.blueprint(registry_bp)

if __name__ == '__main__':
    server.run()
