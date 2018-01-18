# -*- coding: utf-8 -*-
import sys
import getopt

from asyncpg import create_pool

from sanic import Sanic

from jie.environment import Environment

app = Sanic(__name__)


@app.listener('before_server_start')
async def register_db(app, loop):
    env = getattr(app, 'env', None)
    if not env:
        env = Environment(app, loop)
        app.env = env
    if 'DB_CONFIG' not in app.config:
        return
    if 'max_size' not in app.config.DB_CONFIG:
        app.config.DB_CONFIG['max_size'] = 100
    db_pool = await create_pool(**app.config.DB_CONFIG, loop=loop)
    env.db_pool = db_pool


if __name__ == '__main__':
    config_name = 'config.py'
    try:
        options, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config="])
    except getopt.GetoptError:
        sys.exit()
    for name, value in options:
        if name in ('-c', '--config'):
            config_name = value
    app.config.from_pyfile(config_name)
    server_config = app.config.get('SERVER_CONFIG', {'host': '0.0.0.0', 'port': 8080})
    app.run(host=server_config.get('host', '0.0.0.0'),
            port=server_config.get('port', 8080), 
            debug=False)
