class Environment:

    def __init__(self, app, loop, db_pool=None):
        self._app = app
        self._loop = loop
        self._db_pool = db_pool

    @property
    def app(self):
        return self._app

    @property
    def loop(self):
        return self._loop

    @property
    def db_pool(self):
        return self._db_pool

    @db_pool.setter
    def db_pool(self, db_pool):
        self._db_pool = db_pool
