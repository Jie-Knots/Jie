# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser
from collections import namedtuple

from asyncpg import create_pool
from sanic import Sanic

from jie.environment import Environment
from jie.registry import ServiceRegistry

listen = namedtuple('listen', ['register_db', 'register_service'])
args = None


def get_args():
    global args
    if not args:
        parser = ArgumentParser(prog='jie')
        parser.add_argument('-c', dest='config', type=str, default='config.py')
        args = parser.parse_args()
    return args


class Server:

    listener = listen(True, True)

    def __init__(self, name, app=None, environment=Environment, service_registry=ServiceRegistry):
        self.name = name
        if not app:
            app = Sanic(self.name)
        self._app = app
        self.add_config()
        self.add_host_port()

        self.environment = environment
        self.service_registry = service_registry
    
    @property
    def app(self):
        return self._app

    def add_config(self):
        config_name = 'config.py'
        args = get_args()
        config_name = args.config
        self.app.config.from_pyfile(config_name)

    def add_host_port(self):
        if 'SERVER_CONFIG' in self.app.config:
            host = self.app.config.SERVER_CONFIG.get('host', '0.0.0.0')
            port = self.app.config.SERVER_CONFIG.get('port', 8080)
        else:
            host = '0.0.0.0'
            port = 8080
        self.host = host
        self.port = port

    def add_listener(self):
        for item in self.listener._fields:
            if item and hasattr(self, 'listen_{item}'.format(item=item)):
                getattr(self, 'listen_{item}'.format(item=item))()

    def run(self, debug=False):
        self.add_listener()
        self.app.run(host=self.host, port=self.port, debug=debug)

    def get_env(self, loop):
        """Get environment from app. If environment is not existing, create it.
        """
        env = getattr(self.app, 'env', None)
        if not env:
            env = self.environment(self.app, loop, self.host, self.port)
            self.app.env = env
        return env

    def listen_register_db(self):
        """"""
        @self.app.listener('before_server_start')
        async def register_db(app, loop):
            env = self.get_env(loop)
            if 'DB_CONFIG' not in app.config:
                return
            if 'max_size' not in app.config.DB_CONFIG:
                app.config.DB_CONFIG['max_size'] = 100
            db_pool = await create_pool(**app.config.DB_CONFIG, loop=loop)
            env.db_pool = db_pool

    def listen_register_service(self):
        """"""
        @self.app.listener('after_server_start')
        async def register_service(app, loop):
            env = self.get_env(loop)
            if 'REGISTRY_SERVICE_CONFIG' not in app.config:
                return
            host = app.config.REGISTRY_SERVICE_CONFIG.get('host', '0.0.0.0')
            port = app.config.REGISTRY_SERVICE_CONFIG.get('port', 8081)
            registry = ServiceRegistry(app, loop, host, port)
            env.registry = registry
            await registry.registry_service(env)
    

if __name__ == '__main__':
    server = Server('jie')
    server.run()
