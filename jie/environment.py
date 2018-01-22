class Environment:

    def __init__(self, app, loop, host, port):
        self._app = app
        self._loop = loop
        self._host = host
        self._port = port

    @property
    def app(self):
        return self._app

    @property
    def loop(self):
        return self._loop

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def db_pool(self):
        return self._db_pool

    @db_pool.setter
    def db_pool(self, db_pool):
        self._db_pool = db_pool

    @property
    def registry(self):
        return self._registry

    @registry.setter
    def registry(self, registry):
        self._registry = registry
