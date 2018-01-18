# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser

from asyncpg import create_pool

from sanic import Sanic

from jie.environment import Environment

app = Sanic(__name__)
args = None


def get_args():
    global args
    if not args:
        parser = ArgumentParser(prog='jie')
        parser.add_argument('-c', dest='config', type=str, default='config.py')
        args = parser.parse_args()
    return args


def add_config(app):
    config_name = 'config.py'
    args = get_args()
    config_name = args.config
    app.config.from_pyfile(config_name)


def get_env(app, loop):
    """Get environment from app. If environment is not existing, create it.
    """
    env = getattr(app, 'env', None)
    if not env:
        env = Environment(app, loop)
        app.env = env
    return env


@app.listener('before_server_start')
async def register_db(app, loop):
    env = get_env(app, loop)
    if 'DB_CONFIG' not in app.config:
        return
    if 'max_size' not in app.config.DB_CONFIG:
        app.config.DB_CONFIG['max_size'] = 100
    db_pool = await create_pool(**app.config.DB_CONFIG, loop=loop)
    env.db_pool = db_pool


def run(app):
    add_config(app)
    server_config = app.config.get('SERVER_CONFIG', {'host': '0.0.0.0', 'port': 8080})
    app.run(host=server_config.get('host', '0.0.0.0'),
            port=server_config.get('port', 8080), 
            debug=False)


if __name__ == '__main__':
    run(app)
