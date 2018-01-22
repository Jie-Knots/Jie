import aiohttp


class ServiceRegistry:

    def __init__(self, app, loop, host, port=None):
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

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    async def registry_service(self, env):
        async with aiohttp.ClientSession() as session:  
            routes = self.app.router.routes_all.keys()
            app_host = env.host
            app_port = env.port
            app_name = self.app.name
            registry_data = {'routes': routes, 
                             'service_info': {'host': app_host, 'port': app_port, 'name': app_name}}
            url = 'http://{app_host}{app_port}/registry_service'.format(app_host=app_host, app_port=app_port)
            async with session.post(url=url, json=registry_data) as resp:
                pass
